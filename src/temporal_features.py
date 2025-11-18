"""
Temporal Feature Engineering for Player-Centric Analysis

This module provides functions for transforming battle-centric data into
player-centric timelines with temporal and behavioral features.

Key Features:
- Player timeline construction
- Temporal feature engineering (return gaps, streaks)
- Behavioral tilt calculation
- Player-level aggregation
"""

import pandas as pd
import numpy as np
from datetime import timedelta
from typing import Optional, Dict, List


def create_player_timeline_from_battles(battles_df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert battle-centric data to player-centric timelines.

    Each battle becomes TWO rows (winner's perspective + loser's perspective).

    Args:
        battles_df: DataFrame with battle data (winner/loser columns)

    Returns:
        DataFrame with player timelines (player_tag, battleTime, outcome, etc.)
    """
    # Winner's perspective
    winners = battles_df[[
        'winner.tag', 'battleTime',
        'winner.startingTrophies', 'winner.trophyChange', 'winner.crowns',
        'loser.startingTrophies', 'gameMode.id', 'arena.id'
    ]].copy()

    winners.columns = [
        'player_tag', 'battleTime',
        'trophies_before', 'trophy_change', 'crowns',
        'opponent_trophies', 'game_mode', 'arena'
    ]
    winners['outcome'] = 1  # Win

    # Loser's perspective
    losers = battles_df[[
        'loser.tag', 'battleTime',
        'loser.startingTrophies', 'loser.trophyChange', 'loser.crowns',
        'winner.startingTrophies', 'gameMode.id', 'arena.id'
    ]].copy()

    losers.columns = [
        'player_tag', 'battleTime',
        'trophies_before', 'trophy_change', 'crowns',
        'opponent_trophies', 'game_mode', 'arena'
    ]
    losers['outcome'] = 0  # Loss

    # Combine
    player_timeline = pd.concat([winners, losers], ignore_index=True)

    # Remove nulls
    player_timeline = player_timeline.dropna(subset=['player_tag'])

    # Sort by player and time (CRITICAL for temporal features)
    player_timeline = player_timeline.sort_values(
        ['player_tag', 'battleTime']
    ).reset_index(drop=True)

    # Convert battleTime to datetime if string
    if player_timeline['battleTime'].dtype == 'object':
        player_timeline['battleTime'] = pd.to_datetime(player_timeline['battleTime'])

    return player_timeline


def engineer_temporal_features(player_timeline: pd.DataFrame) -> pd.DataFrame:
    """
    Add temporal features to player timeline.

    Features added:
    - next_battleTime: Timestamp of next battle
    - return_gap_hours: Hours between battles
    - fast_return_1hr: Boolean, returned within 1 hour
    - loss_streak: Current consecutive losses
    - win_streak: Current consecutive wins
    - loss_streak_bucket: Categorical loss streak

    Args:
        player_timeline: Sorted DataFrame with player_tag, battleTime, outcome

    Returns:
        DataFrame with added temporal features
    """
    df = player_timeline.copy()

    # Ensure sorted
    df = df.sort_values(['player_tag', 'battleTime'])

    # Group by player
    grouped = df.groupby('player_tag')

    # 1. Next battle time
    df['next_battleTime'] = grouped['battleTime'].shift(-1)

    # 2. Return gap (in hours)
    df['return_gap_hours'] = (
        (df['next_battleTime'] - df['battleTime']).dt.total_seconds() / 3600
    )

    # 3. Fast return (< 1 hour)
    df['fast_return_1hr'] = (df['return_gap_hours'] < 1.0).fillna(False)

    # 4. Loss streaks
    def calculate_loss_streaks(group):
        """Calculate current loss streak at each battle"""
        streaks = []
        current_streak = 0

        for outcome in group['outcome']:
            if outcome == 0:  # Loss
                current_streak += 1
            else:  # Win
                current_streak = 0
            streaks.append(current_streak)

        return pd.Series(streaks, index=group.index)

    df['loss_streak'] = grouped.apply(
        calculate_loss_streaks
    ).reset_index(level=0, drop=True)

    # 5. Win streaks
    def calculate_win_streaks(group):
        """Calculate current win streak at each battle"""
        streaks = []
        current_streak = 0

        for outcome in group['outcome']:
            if outcome == 1:  # Win
                current_streak += 1
            else:  # Loss
                current_streak = 0
            streaks.append(current_streak)

        return pd.Series(streaks, index=group.index)

    df['win_streak'] = grouped.apply(
        calculate_win_streaks
    ).reset_index(level=0, drop=True)

    # 6. Loss streak buckets
    def bucket_loss_streak(streak):
        if streak == 0:
            return "0"
        elif streak <= 2:
            return "1-2"
        elif streak <= 5:
            return "3-5"
        elif streak <= 10:
            return "6-10"
        else:
            return "10+"

    df['loss_streak_bucket'] = df['loss_streak'].apply(bucket_loss_streak)

    return df


def calculate_behavioral_tilt_per_player(player_timeline: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate behavioral tilt score for each player.

    Tilt = % of losses followed by fast return (< 1 hour)
    High tilt = emotional, reactive behavior

    Args:
        player_timeline: DataFrame with player_tag, outcome, fast_return_1hr, next_battleTime

    Returns:
        DataFrame with columns: player_tag, behavioral_tilt_score
    """
    def calculate_tilt(group):
        # Filter to losses only
        losses = group[group['outcome'] == 0].copy()

        if len(losses) == 0:
            return 0.0

        # Exclude last battle (no next battle to measure)
        losses_with_next = losses[losses['next_battleTime'].notna()]

        if len(losses_with_next) == 0:
            return 0.0

        # Count fast returns after losses
        fast_returns_after_loss = losses_with_next['fast_return_1hr'].sum()

        # Tilt score
        tilt_score = fast_returns_after_loss / len(losses_with_next)
        return tilt_score

    tilt_scores = player_timeline.groupby('player_tag').apply(
        calculate_tilt
    ).reset_index()

    tilt_scores.columns = ['player_tag', 'behavioral_tilt_score']

    return tilt_scores


def aggregate_to_player_level(
    player_timeline: pd.DataFrame,
    min_matches: int = 10
) -> pd.DataFrame:
    """
    Aggregate player timeline to player-level features.

    Args:
        player_timeline: Timeline with temporal features
        min_matches: Minimum number of matches required (default: 10)

    Returns:
        DataFrame with one row per player, aggregated features
    """
    # Filter to active players
    match_counts = player_timeline.groupby('player_tag').size()
    active_players = match_counts[match_counts >= min_matches].index

    filtered = player_timeline[player_timeline['player_tag'].isin(active_players)]

    # Aggregate
    aggregated = filtered.groupby('player_tag').agg({
        # Count
        'battleTime': 'count',

        # Performance
        'outcome': 'mean',
        'trophy_change': 'sum',
        'trophies_before': ['first', 'last'],

        # Behavioral
        'return_gap_hours': ['mean', 'median', 'std'],
        'fast_return_1hr': 'mean',
        'loss_streak': 'max',
        'win_streak': 'max',

        # Time span
        'battleTime': ['min', 'max'],
    }).reset_index()

    # Flatten column names
    aggregated.columns = [
        'player_tag',
        'match_count',
        'win_rate',
        'total_trophy_change',
        'starting_trophies',
        'ending_trophies',
        'avg_return_gap_hours',
        'median_return_gap_hours',
        'std_return_gap_hours',
        'fast_return_rate',
        'max_loss_streak',
        'max_win_streak',
        'first_battle',
        'last_battle',
    ]

    # Additional derived features
    aggregated['days_active'] = (
        (aggregated['last_battle'] - aggregated['first_battle']).dt.total_seconds() / 86400
    )

    aggregated['trophy_momentum'] = (
        aggregated['ending_trophies'] - aggregated['starting_trophies']
    )

    aggregated['avg_matches_per_day'] = (
        aggregated['match_count'] / aggregated['days_active'].clip(lower=1)
    )

    return aggregated


def calculate_tilt_by_loss_streak(player_timeline: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze behavioral tilt by loss streak length.

    This shows the key pattern: tilt spikes at 2-3 losses, collapses at 7-10+

    Args:
        player_timeline: Timeline with loss_streak_bucket, fast_return_1hr

    Returns:
        DataFrame with tilt metrics by loss streak bucket
    """
    # Group by loss streak bucket
    tilt_by_streak = player_timeline.groupby('loss_streak_bucket').agg({
        'fast_return_1hr': 'mean',
        'return_gap_hours': 'median',
        'player_tag': 'count',
    }).reset_index()

    tilt_by_streak.columns = [
        'loss_streak_bucket',
        'fast_return_rate',
        'median_return_gap_hours',
        'battle_count'
    ]

    # Sort by bucket order
    bucket_order = ["0", "1-2", "3-5", "6-10", "10+"]
    tilt_by_streak['loss_streak_bucket'] = pd.Categorical(
        tilt_by_streak['loss_streak_bucket'],
        categories=bucket_order,
        ordered=True
    )
    tilt_by_streak = tilt_by_streak.sort_values('loss_streak_bucket')

    return tilt_by_streak


def define_churn(
    player_aggregated: pd.DataFrame,
    churn_threshold_days: int = 7
) -> pd.DataFrame:
    """
    Define churn target variable.

    Churn = No battle in last N days of dataset

    Args:
        player_aggregated: Player-level DataFrame with last_battle
        churn_threshold_days: Days without play to be considered churned (default: 7)

    Returns:
        DataFrame with added 'churned' and 'days_since_last_battle' columns
    """
    df = player_aggregated.copy()

    # Find dataset end date
    dataset_end = df['last_battle'].max()

    # Calculate days since last battle
    df['days_since_last_battle'] = (
        (dataset_end - df['last_battle']).dt.total_seconds() / 86400
    )

    # Define churn
    df['churned'] = (df['days_since_last_battle'] > churn_threshold_days).astype(int)

    return df


def prepare_churn_features(
    player_aggregated: pd.DataFrame,
    feature_columns: Optional[List[str]] = None
) -> tuple:
    """
    Prepare features and target for churn prediction model.

    Args:
        player_aggregated: Player-level DataFrame with features and 'churned' column
        feature_columns: List of feature column names (if None, uses default set)

    Returns:
        Tuple of (X, y, feature_names)
    """
    if feature_columns is None:
        # Default feature set
        feature_columns = [
            # Engagement
            'match_count',
            'days_active',
            'avg_return_gap_hours',
            'median_return_gap_hours',
            'fast_return_rate',
            'avg_matches_per_day',

            # Performance
            'win_rate',
            'trophy_momentum',
            'starting_trophies',

            # Behavior
            'behavioral_tilt_score',
            'max_loss_streak',
            'max_win_streak',
        ]

    # Filter to features that exist
    available_features = [f for f in feature_columns if f in player_aggregated.columns]

    # Prepare X and y
    X = player_aggregated[available_features].fillna(0)
    y = player_aggregated['churned']

    return X, y, available_features


def get_player_profile(
    player_aggregated: pd.DataFrame,
    player_tag: str
) -> Dict:
    """
    Get detailed profile for a specific player.

    Args:
        player_aggregated: Player-level DataFrame
        player_tag: Player tag to lookup

    Returns:
        Dictionary with player stats
    """
    player = player_aggregated[player_aggregated['player_tag'] == player_tag]

    if len(player) == 0:
        return None

    player = player.iloc[0]

    profile = {
        'player_tag': player_tag,
        'match_count': int(player['match_count']),
        'win_rate': float(player['win_rate']),
        'avg_return_gap_hours': float(player['avg_return_gap_hours']),
        'behavioral_tilt_score': float(player.get('behavioral_tilt_score', 0)),
        'max_loss_streak': int(player['max_loss_streak']),
        'trophy_momentum': int(player['trophy_momentum']),
        'churned': int(player.get('churned', 0)),
        'churn_risk': 'High' if player.get('churned', 0) == 1 else 'Low',
    }

    return profile


# Export all functions
__all__ = [
    'create_player_timeline_from_battles',
    'engineer_temporal_features',
    'calculate_behavioral_tilt_per_player',
    'aggregate_to_player_level',
    'calculate_tilt_by_loss_streak',
    'define_churn',
    'prepare_churn_features',
    'get_player_profile',
]
