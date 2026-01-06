class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None

    def height(self, node):
        if not node:
            return 0
        return node.height

    def balance_factor(self, node):
        if not node:
            return 0
        return self.height(node.left) - self.height(node.right)

    def update_height(self, node):
        if not node:
            return
        node.height = 1 + max(self.height(node.left), self.height(node.right))

    def rotate_right(self, z):
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        self.update_height(z)
        self.update_height(y)

        return y

    def rotate_left(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        self.update_height(z)
        self.update_height(y)

        return y

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        # Inserção normal BST
        if not node:
            return Node(key)

        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        else:
            return node  # Chaves duplicadas não são permitidas

        # Atualiza altura
        self.update_height(node)

        # Calcula fator de balanceamento
        balance = self.balance_factor(node)

        # Caso Left-Left
        if balance > 1 and key < node.left.key:
            return self.rotate_right(node)

        # Caso Right-Right
        if balance < -1 and key > node.right.key:
            return self.rotate_left(node)

        # Caso Left-Right
        if balance > 1 and key > node.left.key:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        # Caso Right-Left
        if balance < -1 and key < node.right.key:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if not node:
            return node

        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # Nó com um filho ou sem filhos
            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            # Nó com dois filhos: pega o sucessor
            temp = self._min_value_node(node.right)
            node.key = temp.key
            node.right = self._delete(node.right, temp.key)

        if not node:
            return node

        # Atualiza altura
        self.update_height(node)

        # Rebalanceia
        balance = self.balance_factor(node)

        # Caso Left-Left
        if balance > 1 and self.balance_factor(node.left) >= 0:
            return self.rotate_right(node)

        # Caso Left-Right
        if balance > 1 and self.balance_factor(node.left) < 0:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        # Caso Right-Right
        if balance < -1 and self.balance_factor(node.right) <= 0:
            return self.rotate_left(node)

        # Caso Right-Left
        if balance < -1 and self.balance_factor(node.right) > 0:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    def _min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        if not node or node.key == key:
            return node

        if key < node.key:
            return self._search(node.left, key)
        return self._search(node.right, key)

    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.key)
            self._inorder(node.right, result)

    def print_tree(self, node=None, level=0, prefix="Root: "):
        if node is None:
            node = self.root

        if node:
            print(" " * (level * 4) + prefix + str(node.key) +
                  f" (h={node.height}, bf={self.balance_factor(node)})")
            if node.left or node.right:
                if node.left:
                    self.print_tree(node.left, level + 1, "L--- ")
                else:
                    print(" " * ((level + 1) * 4) + "L--- None")

                if node.right:
                    self.print_tree(node.right, level + 1, "R--- ")
                else:
                    print(" " * ((level + 1) * 4) + "R--- None")


def menu():
    avl = AVLTree()

    while True:
        print("\n" + "=" * 50)
        print("ÁRVORE AVL - MENU INTERATIVO")
        print("=" * 50)
        print("1. Inserir elemento")
        print("2. Deletar elemento")
        print("3. Buscar elemento")
        print("4. Mostrar árvore")
        print("5. Percurso em ordem")
        print("6. Sair")
        print("=" * 50)

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            try:
                valor = int(input("Digite o valor a inserir: "))
                avl.insert(valor)
                print(f"\n✓ Elemento {valor} inserido com sucesso!")
                avl.print_tree()
            except ValueError:
                print("\n✗ Erro: Digite um número inteiro válido!")

        elif opcao == "2":
            try:
                valor = int(input("Digite o valor a deletar: "))
                if avl.search(valor):
                    avl.delete(valor)
                    print(f"\n✓ Elemento {valor} deletado com sucesso!")
                    avl.print_tree()
                else:
                    print(f"\n✗ Elemento {valor} não encontrado na árvore!")
            except ValueError:
                print("\n✗ Erro: Digite um número inteiro válido!")

        elif opcao == "3":
            try:
                valor = int(input("Digite o valor a buscar: "))
                resultado = avl.search(valor)
                if resultado:
                    print(f"\n✓ Elemento {valor} encontrado na árvore!")
                else:
                    print(f"\n✗ Elemento {valor} não encontrado na árvore!")
            except ValueError:
                print("\n✗ Erro: Digite um número inteiro válido!")

        elif opcao == "4":
            if avl.root:
                print("\nEstrutura da árvore:")
                avl.print_tree()
            else:
                print("\n✗ A árvore está vazia!")

        elif opcao == "5":
            if avl.root:
                print("\nPercurso em ordem:", avl.inorder())
            else:
                print("\n✗ A árvore está vazia!")

        elif opcao == "6":
            print("\nEncerrando programa... Até logo!")
            break

        else:
            print("\n✗ Opção inválida! Tente novamente.")


# Executa o menu interativo
if __name__ == "__main__":
    menu()