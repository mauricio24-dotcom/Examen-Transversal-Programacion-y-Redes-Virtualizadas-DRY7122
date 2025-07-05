#Imprime nombres y apellidos integrantes del grupo
def main():
    integrantes = [
        "Mauricio Torres",
        "Vicente Vidal",
    ]
    print("Integrantes del grupo:")
    for nombre in integrantes:
        print(f"- {nombre}")

if __name__ == "__main__":
    main()