import ast
import sys
import os

class AdvancedTradingASTValidator(ast.NodeVisitor):
    def __init__(self, filepath):
        self.filepath = filepath
        self.errors = []
        self.warnings = []
        self.current_function = None

    def visit_FunctionDef(self, node):
        self.current_function = node.name
        
        # 1. Regra de Clean Code: Toda função deve ter Docstring
        if not ast.get_docstring(node):
            self.warnings.append(f"[{self.filepath}] Função '{node.name}' (linha {node.lineno}): Falta de documentação (Docstring).")

        # 2. Análise de Complexidade Ciclomática (Contagem de ifs/whiles/for aninhados)
        complexity = sum(1 for child in ast.walk(node) if isinstance(child, (ast.If, ast.While, ast.For, ast.Try)))
        if complexity > 5:
            self.warnings.append(f"[{self.filepath}] Função '{node.name}' (linha {node.lineno}): Alta complexidade ciclomática ({complexity}). Considere refatorar.")

        self.generic_visit(node)
        self.current_function = None

    def visit_Assign(self, node):
        # 3. Auditoria de Segurança de Risco (Imutabilidade de Variáveis Críticas)
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id in ['risk_max', 'risco_maximo_porcentagem']:
                # Verifica se o valor atribuído é maior que o teto seguro (ex: 0.05 / 5%)
                if isinstance(node.value, ast.Constant) and isinstance(node.value.value, (int, float)):
                    if node.value.value > 0.05:
                        self.errors.append(f"[{self.filepath}] VIOLAÇÃO DE RISCO CRÍTICA (linha {node.lineno}): Tentativa de definir risco máximo acima de 5% ({node.value.value}).")
        self.generic_visit(node)

    def visit_Try(self, node):
        # 4. Clean Code: Proibir blocos try/except genéricos vazios (pass ou omitidos)
        for handler in node.handlers:
            if len(handler.body) == 1 and isinstance(handler.body[0], ast.Pass):
                self.warnings.append(f"[{self.filepath}] Alerta de Resiliência (linha {node.lineno}): Bloco 'except' vazio encontrado (tratamento silencioso de erro).")
        self.generic_visit(node)

def run_ast_audit_pipeline():
    print("=" * 60)
    print("INSPEÇÃO AVANÇADA DE CÓDIGO POR AST (SAST / CODE REVIEW)")
    print("=" * 60)
    
    diretorios = ['domain', 'services', 'strategy', '.']
    arquivos_analisados = 0
    total_erros = 0
    total_avisos = 0

    for d in diretorios:
        if not os.path.exists(d):
            continue
        for root, _, files in os.walk(d):
            # Ignora o ambiente virtual venv
            if 'venv' in root:
                continue
            for file in files:
                if file.endswith('.py'):
                    filepath = os.path.join(root, file)
                    arquivos_analisados += 1
                    
                    with open(filepath, 'r', encoding='utf-8') as f:
                        try:
                            tree = ast.parse(f.read(), filename=filepath)
                            validator = AdvancedTradingASTValidator(filepath)
                            validator.visit(tree)
                            
                            total_erros += len(validator.errors)
                            total_avisos += len(validator.warnings)
                            
                            for err in validator.errors:
                                print(f"❌ [ERRO DE SEGURANÇA] {err}")
                            for warn in validator.warnings:
                                print(f"⚠️  [AVISO CLEAN CODE] {warn}")
                                
                        except SyntaxError as e:
                            print(f"❌ [ERRO DE SINTAXE] Arquivo {filepath} possui erro de compilação: {e}")
                            total_erros += 1

    print("-" * 60)
    print(f"Arquivos analisados via AST: {arquivos_analisados}")
    print(f"Total de Erros Críticos: {total_erros}")
    print(f"Total de Alvisos de Clean Code: {total_avisos}")
    print("=" * 60)

    # Se houver erros críticos de segurança ou risco, o script encerra com código de falha (ideal para CI/CD)
    if total_erros > 0:
        sys.exit(1)
    else:
        print("✔️ Pipeline AST aprovado com sucesso! Código seguro para execução.")
        sys.exit(0)

if __name__ == "__main__":
    run_ast_audit_pipeline()
