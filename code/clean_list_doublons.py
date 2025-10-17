#!/usr/bin/env python3
import json
from typing import List, Any

def remove_duplicates_from_list(input_list: List[Any]) -> List[Any]:
    """
    Supprime les doublons d'une liste tout en conservant l'ordre.
    """
    return list(dict.fromkeys(input_list))

def main(input_file: str, output_file: str) -> None:
    """
    Lit une liste depuis un fichier JSON, supprime les doublons,
    et écrit le résultat dans un nouveau fichier.
    """
    try:
        # Lecture du fichier JSON
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Vérifie que data est bien une liste
        if not isinstance(data, list):
            raise ValueError("Le fichier JSON doit contenir une liste.")

        # Suppression des doublons
        cleaned_data = remove_duplicates_from_list(data)

        # Écriture du résultat dans un nouveau fichier
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(cleaned_data, f, indent=4, ensure_ascii=False)

        print(f"Les doublons ont été supprimés et le résultat a été enregistré dans {output_file}.")

    except Exception as e:
        print(f"Une erreur est survenue : {e}")

if __name__ == "__main__":
    import sys

    if len(sys.argv) == 1:
        print("Usage:  python clean_list_doublons.py <fichier_entree.json> <fichier_sortie.json>")
        print("Or use: python clean_list_doublons.py <fichier_entree_sortie.json>")
        sys.exit(1)

    input_file = sys.argv[1]
    try:
        output_file = sys.argv[2]
    except Exception as e:
        # print(e)
        output_file = input_file
    

    main(input_file, output_file)
