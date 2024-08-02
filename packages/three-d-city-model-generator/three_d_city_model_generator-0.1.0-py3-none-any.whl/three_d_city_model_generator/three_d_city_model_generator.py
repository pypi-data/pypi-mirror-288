"""Main module."""
from rich.console import Console

console = Console()

def generate_model(city_name: str, output_format: str = "obj"):
    """Generate a 3D city model."""
    console.print(f"Generating 3D model for [bold]{city_name}[/bold] in {output_format} format...")
    # Placeholder for actual generation logic
    console.print("Model generation complete!", style="bold green")

if __name__ == "__main__":
    generate_model("Sample City")