"""
Feature Engineering Functions

Functions for creating derived features from battle data.
"""

import pandas as pd
import numpy as np
from typing import List, Tuple


def calculate_deck_complexity(
    elixir_avg: float,
    spell_count: int,
    legendary_count: int
) -> float:
    """
    Calculate a deck complexity score.

    Args:
        elixir_avg: Average elixir cost of the deck
        spell_count: Number of spell cards
        legendary_count: Number of legendary cards

    Returns:
        Complexity score (higher = more complex)
    """
    # Normalize components
    elixir_norm = elixir_avg / 5.0  # Assume max ~5
    spell_norm = spell_count / 8.0
    legendary_norm = legendary_count / 8.0

    # Weighted sum
    complexity = (0.4 * elixir_norm +
                  0.3 * spell_norm +
                  0.3 * legendary_norm)

    return complexity


def extract_card_columns(df: pd.DataFrame, player: str = 'winner') -> List[str]:
    """
    Extract card ID columns for a player.

    Args:
        df: Battle DataFrame
        player: 'winner' or 'loser'

    Returns:
        List of column names like ['winner.card1.id', 'winner.card2.id', ...]
    """
    card_cols = [f'{player}.card{i}.id' for i in range(1, 9)]
    return [col for col in card_cols if col in df.columns]


def create_card_level_features(df: pd.DataFrame, player: str = 'winner') -> pd.DataFrame:
    """
    Create aggregated card level features.

    Args:
        df: Battle DataFrame
        player: 'winner' or 'loser'

    Returns:
        DataFrame with new columns: avg_card_level, min_card_level, max_card_level
    """
    level_cols = [f'{player}.card{i}.level' for i in range(1, 9)]
    level_cols = [col for col in level_cols if col in df.columns]

    result = df.copy()
    result[f'{player}_avg_card_level'] = df[level_cols].mean(axis=1)
    result[f'{player}_min_card_level'] = df[level_cols].min(axis=1)
    result[f'{player}_max_card_level'] = df[level_cols].max(axis=1)
    result[f'{player}_level_std'] = df[level_cols].std(axis=1)

    return result


def create_deck_archetype_features(df: pd.DataFrame, player: str = 'winner') -> pd.DataFrame:
    """
    Create deck archetype features based on card composition.

    Args:
        df: Battle DataFrame with columns like 'winner.troop.count', 'winner.spell.count'
        player: 'winner' or 'loser'

    Returns:
        DataFrame with new archetype indicator columns
    """
    result = df.copy()

    # Spell-heavy deck (3+ spells)
    if f'{player}.spell.count' in df.columns:
        result[f'{player}_spell_heavy'] = (df[f'{player}.spell.count'] >= 3).astype(int)

    # Beatdown deck (high avg elixir)
    if f'{player}.elixir.average' in df.columns:
        result[f'{player}_beatdown'] = (df[f'{player}.elixir.average'] >= 4.0).astype(int)

    # Cycle deck (low avg elixir)
    if f'{player}.elixir.average' in df.columns:
        result[f'{player}_cycle'] = (df[f'{player}.elixir.average'] <= 3.0).astype(int)

    # Building-heavy deck (2+ structures)
    if f'{player}.structure.count' in df.columns:
        result[f'{player}_building_heavy'] = (df[f'{player}.structure.count'] >= 2).astype(int)

    return result


def create_trophy_bracket_features(df: pd.DataFrame, brackets: List[int] = None) -> pd.DataFrame:
    """
    Create trophy bracket categorical features.

    Args:
        df: Battle DataFrame with 'average.startingTrophies' column
        brackets: List of trophy thresholds (default: [0, 1000, 2000, 3000, 4000, 5000, 6000, 8000])

    Returns:
        DataFrame with new 'trophy_bracket' column
    """
    if brackets is None:
        brackets = [0, 1000, 2000, 3000, 4000, 5000, 6000, 8000, 10000]

    result = df.copy()

    if 'average.startingTrophies' in df.columns:
        result['trophy_bracket'] = pd.cut(
            df['average.startingTrophies'],
            bins=brackets,
            labels=[f'{brackets[i]}-{brackets[i+1]}' for i in range(len(brackets)-1)]
        )

    return result


def create_matchup_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create features comparing winner vs loser attributes.

    Args:
        df: Battle DataFrame

    Returns:
        DataFrame with new matchup comparison columns
    """
    result = df.copy()

    # Trophy differential
    if 'winner.startingTrophies' in df.columns and 'loser.startingTrophies' in df.columns:
        result['trophy_diff'] = df['winner.startingTrophies'] - df['loser.startingTrophies']

    # Elixir differential
    if 'winner.elixir.average' in df.columns and 'loser.elixir.average' in df.columns:
        result['elixir_diff'] = df['winner.elixir.average'] - df['loser.elixir.average']

    # Card level differential
    if 'winner.totalcard.level' in df.columns and 'loser.totalcard.level' in df.columns:
        result['card_level_diff'] = df['winner.totalcard.level'] - df['loser.totalcard.level']

    # Spell count differential
    if 'winner.spell.count' in df.columns and 'loser.spell.count' in df.columns:
        result['spell_diff'] = df['winner.spell.count'] - df['loser.spell.count']

    return result


def create_tower_damage_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create features related to tower damage and crown wins.

    Args:
        df: Battle DataFrame

    Returns:
        DataFrame with tower damage-related features
    """
    result = df.copy()

    # Crown differential
    if 'winner.crowns' in df.columns and 'loser.crowns' in df.columns:
        result['crown_diff'] = df['winner.crowns'] - df['loser.crowns']

    # Close game indicator (crown difference <= 1)
    if 'crown_diff' in result.columns:
        result['close_game'] = (result['crown_diff'].abs() <= 1).astype(int)

    # Three-crown win
    if 'winner.crowns' in df.columns:
        result['three_crown_win'] = (df['winner.crowns'] == 3).astype(int)

    return result


def get_card_synergy_pairs(df: pd.DataFrame, player: str = 'winner') -> pd.DataFrame:
    """
    Extract all unique card pairs from decks.

    Args:
        df: Battle DataFrame
        player: 'winner' or 'loser'

    Returns:
        DataFrame with columns: battle_index, card_1, card_2
    """
    card_cols = extract_card_columns(df, player)

    pairs = []
    for idx, row in df.iterrows():
        cards = [row[col] for col in card_cols if pd.notna(row[col])]
        # Generate all pairs
        for i in range(len(cards)):
            for j in range(i+1, len(cards)):
                pairs.append({
                    'battle_index': idx,
                    'card_1': min(cards[i], cards[j]),  # Sorted to avoid duplicates
                    'card_2': max(cards[i], cards[j]),
                    'won': 1 if player == 'winner' else 0
                })

    return pd.DataFrame(pairs)


def calculate_lift(
    pair_win_rate: float,
    card1_win_rate: float,
    card2_win_rate: float
) -> float:
    """
    Calculate lift metric for card synergy.

    Lift > 1 means the pair performs better together than expected.

    Args:
        pair_win_rate: Win rate when both cards are in deck
        card1_win_rate: Win rate of card 1 overall
        card2_win_rate: Win rate of card 2 overall

    Returns:
        Lift value
    """
    expected_win_rate = card1_win_rate * card2_win_rate

    if expected_win_rate == 0:
        return 0

    lift = pair_win_rate / expected_win_rate

    return lift
