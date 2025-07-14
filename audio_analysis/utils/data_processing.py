"""
Data Processing Utilities for Audio Analysis

This module provides utilities for processing and cleaning audio analysis data.
It handles common data transformation tasks, standardization, and preparation
for machine learning algorithms.

Key functions:
- Feature standardization and normalization
- Data cleaning and validation
- DataFrame manipulation and preparation
- Missing value handling
- Outlier detection and treatment
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.impute import SimpleImputer
import warnings


class DataProcessor:
    """
    Comprehensive data processing utility for audio analysis.
    
    This class provides methods for cleaning, standardizing, and preparing
    audio analysis data for machine learning and visualization. It handles
    common data quality issues and ensures consistent data formats.
    """
    
    def __init__(self):
        """Initialize the data processor with default settings."""
        self.scaler = StandardScaler()
        self.imputer = SimpleImputer(strategy='mean')
        self.feature_names = None
        self.numeric_columns = None
        
    def clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and validate a DataFrame containing audio analysis results.
        
        This method performs comprehensive data cleaning:
        1. Handles missing values appropriately
        2. Removes or corrects invalid data points
        3. Standardizes data types
        4. Validates numeric ranges
        5. Removes duplicate entries
        
        The cleaning process is designed to be robust against common issues
        that arise in audio analysis, such as feature extraction failures,
        infinite values from mathematical operations, and inconsistent data types.
        
        Args:
            df: DataFrame to clean
            
        Returns:
            Cleaned DataFrame
        """
        if df.empty:
            return df
        
        # Create a copy to avoid modifying the original
        cleaned_df = df.copy()
        
        # Stage 1: Remove duplicate entries
        # Duplicates can occur when processing files multiple times
        before_count = len(cleaned_df)
        cleaned_df = cleaned_df.drop_duplicates(subset=['filename'] if 'filename' in cleaned_df.columns else None)
        if len(cleaned_df) < before_count:
            print(f"Removed {before_count - len(cleaned_df)} duplicate entries")
        
        # Stage 2: Handle infinite and NaN values
        # These commonly occur in spectral analysis when dividing by zero
        # or taking logarithms of zero values
        numeric_columns = cleaned_df.select_dtypes(include=[np.number]).columns
        
        # Replace infinite values with NaN for consistent handling
        cleaned_df[numeric_columns] = cleaned_df[numeric_columns].replace([np.inf, -np.inf], np.nan)
        
        # Count missing values before cleaning
        missing_counts = cleaned_df[numeric_columns].isnull().sum()
        if missing_counts.sum() > 0:
            print(f"Found {missing_counts.sum()} missing values across {len(missing_counts[missing_counts > 0])} columns")
        
        # Stage 3: Handle missing values intelligently
        # Different strategies for different types of features
        for column in numeric_columns:
            if column in cleaned_df.columns and cleaned_df[column].isnull().sum() > 0:
                # For energy features, use zero as default (represents silence)
                if 'energy' in column.lower() or 'rms' in column.lower():
                    cleaned_df[column] = cleaned_df[column].fillna(0)
                
                # For spectral features, use median (more robust than mean)
                elif 'spectral' in column.lower() or 'centroid' in column.lower():
                    cleaned_df[column] = cleaned_df[column].fillna(cleaned_df[column].median())
                
                # For temporal features, use mean
                elif 'tempo' in column.lower() or 'duration' in column.lower():
                    cleaned_df[column] = cleaned_df[column].fillna(cleaned_df[column].mean())
                
                # For MFCC features, use zero (neutral timbre)
                elif 'mfcc' in column.lower():
                    cleaned_df[column] = cleaned_df[column].fillna(0)
                
                # For other features, use median
                else:
                    cleaned_df[column] = cleaned_df[column].fillna(cleaned_df[column].median())
        
        # Stage 4: Validate and correct data ranges
        # Ensure features are within expected ranges
        cleaned_df = self._validate_feature_ranges(cleaned_df)
        
        # Stage 5: Handle categorical data
        # Ensure string columns are properly formatted
        string_columns = cleaned_df.select_dtypes(include=['object']).columns
        for column in string_columns:
            if column in cleaned_df.columns:
                # Convert to string and strip whitespace
                cleaned_df[column] = cleaned_df[column].astype(str).str.strip()
                
                # Handle empty strings
                cleaned_df[column] = cleaned_df[column].replace('', 'unknown')
                cleaned_df[column] = cleaned_df[column].replace('nan', 'unknown')
        
        # Stage 6: Final validation
        # Ensure no remaining invalid values
        remaining_issues = cleaned_df[numeric_columns].isnull().sum().sum()
        if remaining_issues > 0:
            print(f"Warning: {remaining_issues} values could not be cleaned")
        
        return cleaned_df
    
    def _validate_feature_ranges(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Validate and correct feature ranges.
        
        This method ensures that features are within expected ranges
        based on their physical or mathematical constraints.
        
        Args:
            df: DataFrame to validate
            
        Returns:
            DataFrame with corrected ranges
        """
        # First, ensure all numeric columns are properly converted from any list/array values
        from .type_conversion import safe_float_convert
        
        numeric_columns = df.select_dtypes(include=[np.number, 'object']).columns
        for col in numeric_columns:
            if col in df.columns:
                # Convert any list/array values to float values
                df[col] = df[col].apply(lambda x: safe_float_convert(x) if not isinstance(x, str) else x)
        
        # Tempo should be positive and within reasonable range
        if 'tempo' in df.columns:
            df['tempo'] = pd.to_numeric(df['tempo'], errors='coerce')
            df['tempo'] = df['tempo'].fillna(120)  # Default to 120 BPM
            df['tempo'] = df['tempo'].clip(lower=30, upper=300)
        
        # Duration should be positive
        if 'duration' in df.columns:
            df['duration'] = pd.to_numeric(df['duration'], errors='coerce')
            df['duration'] = df['duration'].fillna(0)  # Default to 0
            df['duration'] = df['duration'].clip(lower=0)
        
        # Energy features should be non-negative
        energy_columns = [col for col in df.columns if 'energy' in col.lower() or 'rms' in col.lower()]
        for col in energy_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col] = df[col].fillna(0)  # Default to 0 for energy features
            df[col] = df[col].clip(lower=0)
        
        # Spectral features should be non-negative
        spectral_columns = [col for col in df.columns if 'spectral' in col.lower()]
        for col in spectral_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            # Fill with median if available, otherwise 0
            median_val = df[col].median()
            if pd.isna(median_val):
                median_val = 0
            df[col] = df[col].fillna(median_val)
            df[col] = df[col].clip(lower=0)
        
        # Zero-crossing rate should be between 0 and 1
        if 'zero_crossing_rate_mean' in df.columns:
            df['zero_crossing_rate_mean'] = pd.to_numeric(df['zero_crossing_rate_mean'], errors='coerce')
            df['zero_crossing_rate_mean'] = df['zero_crossing_rate_mean'].fillna(0.05)  # Default to low roughness
            df['zero_crossing_rate_mean'] = df['zero_crossing_rate_mean'].clip(lower=0, upper=1)
        
        # Phase counts should be positive integers
        if 'num_phases' in df.columns:
            df['num_phases'] = pd.to_numeric(df['num_phases'], errors='coerce')
            df['num_phases'] = df['num_phases'].fillna(1)  # Default to 1 phase
            df['num_phases'] = df['num_phases'].clip(lower=1).astype(int)
        
        # Final check: ensure no NaN values remain in numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if df[col].isna().any():
                # Fill remaining NaN values with column median or 0 if all NaN
                median_val = df[col].median()
                if pd.isna(median_val):
                    median_val = 0
                df[col] = df[col].fillna(median_val)
        
        return df
    
    def standardize_features(self, df: pd.DataFrame, method: str = 'standard') -> Tuple[pd.DataFrame, Any]:
        """
        Standardize numeric features for machine learning.
        
        This method applies standardization to numeric features to ensure
        they have consistent scales. This is crucial for clustering and
        other machine learning algorithms that are sensitive to scale.
        
        Args:
            df: DataFrame with features to standardize
            method: Standardization method ('standard', 'minmax', 'robust')
            
        Returns:
            Tuple of (standardized_dataframe, fitted_scaler)
        """
        if df.empty:
            return df, None
        
        # Select numeric columns for standardization
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        
        # Exclude columns that shouldn't be standardized
        excluded_columns = ['duration', 'num_phases', 'cluster']
        standardization_columns = [col for col in numeric_columns if col not in excluded_columns]
        
        if not standardization_columns:
            return df, None
        
        # Choose scaler based on method
        if method == 'standard':
            scaler = StandardScaler()
        elif method == 'minmax':
            scaler = MinMaxScaler()
        elif method == 'robust':
            scaler = RobustScaler()
        else:
            raise ValueError(f"Unknown standardization method: {method}")
        
        # Create copy for standardization
        standardized_df = df.copy()
        
        # Fit and transform the features
        standardized_values = scaler.fit_transform(df[standardization_columns])
        
        # Replace original values with standardized values
        standardized_df[standardization_columns] = standardized_values
        
        # Store scaler for later use
        self.scaler = scaler
        self.feature_names = standardization_columns
        
        return standardized_df, scaler
    
    def prepare_clustering_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare features specifically for clustering analysis.
        
        This method selects and processes features that are most relevant
        for clustering audio tracks. It removes metadata and focuses on
        musical characteristics.
        
        Args:
            df: DataFrame with all features
            
        Returns:
            DataFrame with clustering-ready features
        """
        if df.empty:
            return df
        
        # Select numeric columns
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        
        # Exclude non-musical features
        excluded_columns = [
            'duration',  # More metadata than musical characteristic
            'cluster',   # Would be circular for clustering
            'phase_number',  # Ordinal, not continuous
            'position'   # Ordinal, not continuous
        ]
        
        # Include only relevant features
        clustering_columns = [col for col in numeric_columns if col not in excluded_columns]
        
        # Create clustering DataFrame
        clustering_df = df[clustering_columns].copy()
        
        # Additional cleaning for clustering
        clustering_df = self._remove_low_variance_features(clustering_df)
        clustering_df = self._handle_correlated_features(clustering_df)
        
        return clustering_df
    
    def _remove_low_variance_features(self, df: pd.DataFrame, threshold: float = 0.001) -> pd.DataFrame:
        """
        Remove features with very low variance.
        
        Low variance features don't contribute much to clustering and
        can add noise to the analysis.
        
        Args:
            df: DataFrame to process
            threshold: Variance threshold for removal
            
        Returns:
            DataFrame with low variance features removed
        """
        if df.empty:
            return df
        
        # Calculate variance for each feature
        variances = df.var()
        
        # Identify low variance features
        low_variance_features = variances[variances < threshold].index.tolist()
        
        if low_variance_features:
            print(f"Removing {len(low_variance_features)} low variance features")
            df = df.drop(columns=low_variance_features)
        
        return df
    
    def _handle_correlated_features(self, df: pd.DataFrame, threshold: float = 0.95) -> pd.DataFrame:
        """
        Handle highly correlated features to reduce redundancy.
        
        Highly correlated features can cause issues in clustering by
        giving excessive weight to similar information.
        
        Args:
            df: DataFrame to process
            threshold: Correlation threshold for removal
            
        Returns:
            DataFrame with correlated features handled
        """
        if df.empty or len(df.columns) <= 1:
            return df
        
        # Calculate correlation matrix
        correlation_matrix = df.corr().abs()
        
        # Find highly correlated pairs
        high_correlation_pairs = []
        for i in range(len(correlation_matrix.columns)):
            for j in range(i+1, len(correlation_matrix.columns)):
                if correlation_matrix.iloc[i, j] > threshold:
                    high_correlation_pairs.append((
                        correlation_matrix.columns[i],
                        correlation_matrix.columns[j],
                        correlation_matrix.iloc[i, j]
                    ))
        
        # Remove one feature from each highly correlated pair
        features_to_remove = set()
        for feature1, feature2, correlation in high_correlation_pairs:
            # Remove the feature with lower variance (less informative)
            if df[feature1].var() < df[feature2].var():
                features_to_remove.add(feature1)
            else:
                features_to_remove.add(feature2)
        
        if features_to_remove:
            print(f"Removing {len(features_to_remove)} highly correlated features")
            df = df.drop(columns=list(features_to_remove))
        
        return df
    
    def create_feature_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Create a summary of features in the DataFrame.
        
        This method provides comprehensive information about the features,
        useful for understanding the data and making processing decisions.
        
        Args:
            df: DataFrame to summarize
            
        Returns:
            Dictionary with feature summary
        """
        if df.empty:
            return {'error': 'DataFrame is empty'}
        
        # Basic statistics
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        categorical_columns = df.select_dtypes(include=['object']).columns
        
        summary = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'numeric_columns': len(numeric_columns),
            'categorical_columns': len(categorical_columns),
            'missing_values': df.isnull().sum().sum(),
            'duplicate_rows': df.duplicated().sum()
        }
        
        # Numeric feature statistics
        if len(numeric_columns) > 0:
            numeric_stats = df[numeric_columns].describe()
            summary['numeric_stats'] = {
                'mean_values': numeric_stats.loc['mean'].to_dict(),
                'std_values': numeric_stats.loc['std'].to_dict(),
                'min_values': numeric_stats.loc['min'].to_dict(),
                'max_values': numeric_stats.loc['max'].to_dict()
            }
        
        # Categorical feature statistics
        if len(categorical_columns) > 0:
            categorical_stats = {}
            for column in categorical_columns:
                categorical_stats[column] = {
                    'unique_values': df[column].nunique(),
                    'most_common': df[column].mode().iloc[0] if not df[column].mode().empty else None,
                    'value_counts': df[column].value_counts().head().to_dict()
                }
            summary['categorical_stats'] = categorical_stats
        
        # Feature quality assessment
        summary['data_quality'] = {
            'completeness': (1 - df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100,
            'consistency': (1 - df.duplicated().sum() / len(df)) * 100,
            'recommendations': self._get_data_quality_recommendations(df)
        }
        
        return summary
    
    def _get_data_quality_recommendations(self, df: pd.DataFrame) -> List[str]:
        """
        Generate recommendations for improving data quality.
        
        Args:
            df: DataFrame to assess
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # Check for missing values
        missing_ratio = df.isnull().sum().sum() / (len(df) * len(df.columns))
        if missing_ratio > 0.05:
            recommendations.append("Consider improving feature extraction to reduce missing values")
        
        # Check for duplicates
        duplicate_ratio = df.duplicated().sum() / len(df)
        if duplicate_ratio > 0.01:
            recommendations.append("Remove duplicate entries to improve analysis quality")
        
        # Check for low variance features
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        if len(numeric_columns) > 0:
            low_variance_count = (df[numeric_columns].var() < 0.001).sum()
            if low_variance_count > 0:
                recommendations.append(f"Consider removing {low_variance_count} low variance features")
        
        # Check for highly correlated features
        if len(numeric_columns) > 1:
            correlation_matrix = df[numeric_columns].corr().abs()
            high_correlation_count = (correlation_matrix > 0.95).sum().sum() - len(correlation_matrix)
            if high_correlation_count > 0:
                recommendations.append("Consider reducing feature redundancy by handling correlated features")
        
        if not recommendations:
            recommendations.append("Data quality looks good!")
        
        return recommendations


def standardize_features(df: pd.DataFrame, method: str = 'standard') -> Tuple[pd.DataFrame, Any]:
    """
    Standalone function for feature standardization.
    
    Args:
        df: DataFrame to standardize
        method: Standardization method
        
    Returns:
        Tuple of (standardized_dataframe, fitted_scaler)
    """
    processor = DataProcessor()
    return processor.standardize_features(df, method)


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standalone function for DataFrame cleaning.
    
    Args:
        df: DataFrame to clean
        
    Returns:
        Cleaned DataFrame
    """
    processor = DataProcessor()
    return processor.clean_dataframe(df)


def prepare_for_export(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare DataFrame for export to various formats.
    
    This function ensures the DataFrame is in the best format for
    export to CSV, JSON, or other formats, with proper data types
    and formatting.
    
    Args:
        df: DataFrame to prepare
        
    Returns:
        Export-ready DataFrame
    """
    if df.empty:
        return df
    
    export_df = df.copy()
    
    # Convert numpy types to Python types for better compatibility
    numeric_columns = export_df.select_dtypes(include=[np.number]).columns
    for column in numeric_columns:
        if export_df[column].dtype in ['int64', 'int32']:
            export_df[column] = export_df[column].astype(int)
        elif export_df[column].dtype in ['float64', 'float32']:
            export_df[column] = export_df[column].astype(float)
    
    # Ensure string columns are properly formatted
    string_columns = export_df.select_dtypes(include=['object']).columns
    for column in string_columns:
        export_df[column] = export_df[column].astype(str)
    
    # Round numeric values to reasonable precision
    float_columns = export_df.select_dtypes(include=['float']).columns
    for column in float_columns:
        if 'mfcc' in column.lower():
            export_df[column] = export_df[column].round(4)
        elif 'spectral' in column.lower():
            export_df[column] = export_df[column].round(2)
        elif 'tempo' in column.lower():
            export_df[column] = export_df[column].round(1)
        else:
            export_df[column] = export_df[column].round(3)
    
    return export_df