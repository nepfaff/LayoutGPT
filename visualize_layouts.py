#!/usr/bin/env python3
"""Simple 2D top-down visualization of generated 3D layouts."""
import json
import os
import argparse
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np

# Color palette for different furniture types
FURNITURE_COLORS = {
    'double_bed': '#FF6B6B',
    'single_bed': '#FF8E8E',
    'kids_bed': '#FFB4B4',
    'wardrobe': '#4ECDC4',
    'nightstand': '#45B7D1',
    'cabinet': '#96CEB4',
    'desk': '#FFEAA7',
    'chair': '#DDA0DD',
    'dressing_table': '#98D8C8',
    'dressing_chair': '#F7DC6F',
    'tv_stand': '#BB8FCE',
    'sofa': '#85C1E9',
    'armchair': '#AED6F1',
    'bookshelf': '#F8B500',
    'shelf': '#FAD7A0',
    'table': '#D7BDE2',
    'stool': '#A9CCE3',
    'floor_lamp': '#F9E79F',
    'ceiling_lamp': '#FCF3CF',
    'pendant_lamp': '#FEF9E7',
    'coffee_table': '#D5DBDB',
    'children_cabinet': '#A3E4D7',
}

def draw_furniture(ax, furniture_name, bbox, room_size=(256, 256)):
    """Draw a single piece of furniture as a rotated rectangle."""
    left = bbox['left']
    top = bbox['top']
    width = bbox['width']
    length = bbox['length']
    orientation = bbox.get('orientation', 0)

    # Get color for this furniture type
    color = FURNITURE_COLORS.get(furniture_name, '#CCCCCC')

    # Create rectangle centered at position, then rotate
    # Note: in the layout, 'left' is x, 'top' is y
    center_x = left
    center_y = top

    # Create a rectangle patch
    rect = patches.Rectangle(
        (center_x - length/2, center_y - width/2),
        length, width,
        linewidth=1,
        edgecolor='black',
        facecolor=color,
        alpha=0.7
    )

    # Apply rotation around center
    t = patches.transforms.Affine2D().rotate_deg_around(center_x, center_y, -orientation) + ax.transData
    rect.set_transform(t)

    ax.add_patch(rect)

    # Add label
    ax.text(center_x, center_y, furniture_name.replace('_', '\n'),
            ha='center', va='center', fontsize=6, fontweight='bold')

def visualize_scene(scene_data, output_path, room_size=(256, 256)):
    """Visualize a single scene."""
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))

    # Draw room boundary
    ax.add_patch(patches.Rectangle(
        (0, 0), room_size[0], room_size[1],
        linewidth=2, edgecolor='black', facecolor='#F5F5F5'
    ))

    # Draw each piece of furniture
    for furniture_name, bbox in scene_data['object_list']:
        draw_furniture(ax, furniture_name, bbox, room_size)

    ax.set_xlim(-20, room_size[0] + 20)
    ax.set_ylim(-20, room_size[1] + 20)
    ax.set_aspect('equal')
    ax.set_title(f"Scene: {scene_data.get('query_id', 'Unknown')}", fontsize=12)
    ax.set_xlabel('X (pixels)')
    ax.set_ylabel('Y (pixels)')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

def main():
    parser = argparse.ArgumentParser(description='Visualize 3D layout predictions as 2D top-down views')
    parser.add_argument('--input', type=str, required=True, help='Path to JSON file with predictions')
    parser.add_argument('--output_dir', type=str, default='./visualizations', help='Output directory for images')
    parser.add_argument('--num_scenes', type=int, default=10, help='Number of scenes to visualize')
    parser.add_argument('--room_size', type=int, default=256, help='Room size in pixels')
    args = parser.parse_args()

    # Load predictions
    with open(args.input, 'r') as f:
        predictions = json.load(f)

    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)

    # Visualize scenes
    num_to_vis = min(args.num_scenes, len(predictions))
    print(f"Visualizing {num_to_vis} scenes...")

    for i, scene in enumerate(predictions[:num_to_vis]):
        scene_id = scene.get('query_id', f'scene_{i}').replace('/', '_')
        output_path = os.path.join(args.output_dir, f'{i:03d}_{scene_id}.png')
        visualize_scene(scene, output_path, (args.room_size, args.room_size))
        print(f"  Saved: {output_path}")

    print(f"\nDone! {num_to_vis} visualizations saved to {args.output_dir}")

if __name__ == '__main__':
    main()
