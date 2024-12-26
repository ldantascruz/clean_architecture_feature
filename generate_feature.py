import os

# Estrutura de pastas e arquivos da feature
FEATURE_STRUCTURE = {
    "domain": {
        "repository": ["_repository.dart", "{feature}.repository.dart"],
        "usecase": ["_usecase.dart"],
        "_domain.dart": None,
    },
    "external": {
        "datasource": ["_datasource.dart", "{feature}.datasource.impl.dart"],
        "_external.dart": None,
    },
    "infra": {
        "datasource": ["_datasource.dart", "{feature}.datasource.dart"],
        "repository": ["_repository.dart", "{feature}.repository.impl.dart"],
        "_infra.dart": None,
    },
    "presentation": {
        "controller": {
            "_controller.dart": None,
            "{feature}.cubit.dart": None,
            "{feature}.state.dart": None,
        },
        "page": {
            "_page.dart": None,
            "{feature}.page.dart": None,
        },
        "widget": {
            "_widget.dart": None,
        },
        "_presentation.dart": None,
    },
    "_{feature}.dart": None,
    "{feature}.router.dart": None,
    "{feature}.setup.locator.dart": None,
}

# Templates de conteúdo para arquivos específicos
ROUTER_TEMPLATE = """
import 'package:go_router/go_router.dart';

import '_{feature}.dart';

extension FullPath on {Feature}RoutesEnum {
  String get fullPath => '${{Feature}Router.basePath}/$routePath';
}

enum {Feature}RoutesEnum {
  {feature}('{feature}', '{feature}');

  const {Feature}RoutesEnum(
    this.routePath,
    this.routeName,
  );

  final String routePath;
  final String routeName;
}

class {Feature}Router {
  {Feature}Router._();

  static const String basePath = '/{feature}';

  static List<RouteBase> routes = [
    GoRoute(
      name: {Feature}RoutesEnum.{feature}.routeName,
      path: {Feature}RoutesEnum.{feature}.fullPath,
      builder: (context, state) => const {Feature}Page(),
    ),
  ];
}
"""

PAGE_TEMPLATE = """
import 'package:flutter/material.dart';
import 'package:get_it/get_it.dart';

import '../../_{feature}.dart';

class {Feature}Page extends StatelessWidget {
  const {Feature}Page({super.key});

  @override
  Widget build(BuildContext context) {
    final cubit = GetIt.I.get<{Feature}Cubit>();
    return const Scaffold();
  }
}
"""

REPOSITORY_TEMPLATE = """
abstract class {Feature}Repository {}
"""

DATASOURCE_IMPL_TEMPLATE = """
import 'package:dio/dio.dart' as dio;

import '../../../../core/_core.dart';
import '../../_{feature}.dart';

class {Feature}DatasourceImpl implements {Feature}Datasource {
    {Feature}DatasourceImpl({required dio.Dio httpClient, required AppStorage storage})
      : _httpClient = httpClient,
        _storage = storage;

  final dio.Dio _httpClient;
  final AppStorage _storage;

  Future<dio.Options> getOptions() async {
    String? token;
    final authResponse = await _storage.getAuthResponse();
    if (authResponse != null) {
      token = authResponse.token;
    }

    final Map<String, dynamic> headers = {
      token != null ? 'Authorization' : '': token != null ? 'Bearer $token' : '',
    };
    return dio.Options(headers: headers, responseType: dio.ResponseType.json);
  }
}
"""

DATASOURCE_TEMPLATE = """
abstract class {Feature}Datasource {}
"""

REPOSITORY_IMPL_TEMPLATE = """
import '../../_{feature}.dart';

class {Feature}RepositoryImpl implements {Feature}Repository {
    {Feature}RepositoryImpl({required {Feature}Datasource datasource}) : _datasource = datasource;

    final {Feature}Datasource _datasource;
}
"""

SETUP_LOCATOR_TEMPLATE = """
import 'package:dio/dio.dart';
import 'package:get_it/get_it.dart';

import '../../core/_core.dart';
import '_{feature}.dart';

class {Feature}SetupLocator {
  void _datasource(GetIt instance) {
    // Registre aqui os datasources
    instance.registerLazySingleton<{Feature}Datasource>(
      () => {Feature}DatasourceImpl(
        httpClient: instance.get<Dio>(),
        storage: instance.get<AppStorage>(),
      ),
    );
  }

  void _repository(GetIt instance) {
    // Registre aqui os repositórios
    instance.registerLazySingleton<{Feature}Repository>(
      () => {Feature}RepositoryImpl(datasource: instance.get<{Feature}Datasource>()),
    );
  }

  void _usecase(GetIt instance) {
    // Registre aqui os casos de uso
  }

  void _cubit(GetIt instance) {
    // Registre aqui os cubits
    instance.registerFactory<{Feature}Cubit>(
      () => {Feature}Cubit(),
    );
  }

  void call(GetIt instance) {
    _datasource(instance);
    _repository(instance);
    _usecase(instance);
    _cubit(instance);
  }
}
"""

STATE_TEMPLATE = """
part of '{feature}.cubit.dart';

abstract class {Feature}State extends Equatable { 
    const {Feature}State();

    @override List<Object> get props => []; 
}

class {Feature}Initial extends {Feature}State {}

class {Feature}Loading extends {Feature}State {}

class {Feature}Success extends {Feature}State {}

class {Feature}KycRequired extends {Feature}State {}

class {Feature}Error extends {Feature}State { 
    final String message;

    const {Feature}Error(this.message);

    @override List<Object> get props => [message]; 
} 
"""

CUBIT_TEMPLATE = """
import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';

part '{feature}.state.dart';

class {Feature}Cubit extends Cubit<{Feature}State> {
{Feature}Cubit() : super({Feature}Initial());
}
"""


EXPORT_TEMPLATES = {
    "_{feature}.dart": [
        "export '{feature}.router.dart';",
        "export '{feature}.setup.locator.dart';",
        "export 'domain/_domain.dart';",
        "export 'external/_external.dart';",
        "export 'infra/_infra.dart';",
        "export 'presentation/_presentation.dart';",
    ],
    "_domain.dart": [
        "export 'repository/_repository.dart';",
        "export 'usecase/_usecase.dart';",
    ],
    "_repository.dart": [
        "export '{feature}.repository.dart';",
    ],
    "_usecase.dart": [
        "export '{feature}.usecase.dart';",
    ],
    "_external.dart": [
        "export 'datasource/_datasource.dart';",
    ],
    "_datasource.dart": [
        "export '{feature}.datasource.dart';",
        "export '{feature}.datasource.impl.dart';",
    ],
    "_infra.dart": [
        "export 'datasource/_datasource.dart';",
        "export 'repository/_repository.dart';",
    ],
    "_presentation.dart": [
        "export 'controller/_controller.dart';",
        "export 'page/_page.dart';",
        "export 'widget/_widget.dart';",
    ],
    "_controller.dart": [
        "export '{feature}.cubit.dart';",
    ],
    "_page.dart": [
        "export '{feature}.page.dart';",
    ],
    "_widget.dart": [],
}


def create_file(filepath, content=""):
    """Cria um arquivo e escreve o conteúdo fornecido."""
    with open(filepath, "w") as f:
        f.write(content)


def add_exports_to_file(filepath, export_lines):
    """Adiciona linhas de exportação ao arquivo."""
    with open(filepath, "w") as f:
        for line in export_lines:
            f.write(f"{line}\n")


def create_feature_structure(base_path, feature_name):
    """
    Cria a estrutura de pastas e arquivos para uma nova feature.
    """
    feature_path = os.path.join(base_path, feature_name)
    os.makedirs(feature_path, exist_ok=True)

    def create_recursive(structure, path):
        for key, value in structure.items():
            if isinstance(value, dict):
                # Cria pasta e chama recursivamente
                folder_path = os.path.join(path, key)
                os.makedirs(folder_path, exist_ok=True)
                create_recursive(value, folder_path)
            elif isinstance(value, list):
                # Cria arquivos dentro da pasta
                folder_path = os.path.join(path, key)
                os.makedirs(folder_path, exist_ok=True)
                for filename in value:
                    filepath = os.path.join(folder_path, filename.replace("{feature}", feature_name))
                    if filename == "{feature}.state.dart":
                        # Gera o arquivo state com o template
                        content = STATE_TEMPLATE.replace("{feature}", feature_name).replace("{Feature}", feature_name.capitalize())
                        create_file(filepath, content)
                    elif filename == "{feature}.cubit.dart":
                        # Gera o arquivo cubit com o template
                        content = CUBIT_TEMPLATE.replace("{feature}", feature_name).replace("{Feature}", feature_name.capitalize())
                        create_file(filepath, content)
                    elif filename == "{feature}.repository.dart":
                        content = REPOSITORY_TEMPLATE.replace("{feature}", feature_name).replace("{Feature}", feature_name.capitalize())
                        create_file(filepath, content)
                    elif filename == "{feature}.datasource.impl.dart":
                        content = DATASOURCE_IMPL_TEMPLATE.replace("{feature}", feature_name).replace("{Feature}", feature_name.capitalize())
                        create_file(filepath, content)
                    elif filename == "{feature}.datasource.dart":
                        content = DATASOURCE_TEMPLATE.replace("{feature}", feature_name).replace("{Feature}", feature_name.capitalize())
                        create_file(filepath, content)
                    elif filename == "{feature}.repository.impl.dart":
                        content = REPOSITORY_IMPL_TEMPLATE.replace("{feature}", feature_name).replace("{Feature}", feature_name.capitalize())
                        create_file(filepath, content)
                    elif filename == "_repository.dart" and "infra" in folder_path:
                        # Adiciona export correto para _repository.dart em infra
                        export_line = f"export '{feature_name}.repository.impl.dart';"
                        add_exports_to_file(filepath, [export_line])
                    elif filename == "_repository.dart" and "domain" in folder_path:
                        # Adiciona export correto para _repository.dart em domain
                        export_line = f"export '{feature_name}.repository.dart';"
                        add_exports_to_file(filepath, [export_line])
                    elif filename == "_datasource.dart" and "external" in folder_path:
                        # Adiciona export correto para _datasource.dart em external
                        export_line = f"export '{feature_name}.datasource.impl.dart';"
                        add_exports_to_file(filepath, [export_line])
                    elif filename == "_datasource.dart" and "infra" in folder_path:
                        # Adiciona export correto para _datasource.dart em infra
                        export_line = f"export '{feature_name}.datasource.dart';"
                        add_exports_to_file(filepath, [export_line])
                    else:
                        create_file(filepath)  # Cria arquivo vazio
            else:
                # Cria arquivo diretamente
                filepath = os.path.join(path, key.replace("{feature}", feature_name))
                if key in EXPORT_TEMPLATES:
                    # Adiciona exports ao arquivo
                    exports = [
                        line.replace("{feature}", feature_name)
                        for line in EXPORT_TEMPLATES[key]
                    ]
                    add_exports_to_file(filepath, exports)
                elif key == "{feature}.router.dart":
                    # Preenche o conteúdo do router.dart
                    content = ROUTER_TEMPLATE.replace("{feature}", feature_name).replace("{Feature}", feature_name.capitalize())
                    create_file(filepath, content)
                elif key == "{feature}.setup.locator.dart":
                    # Preenche o conteúdo do setup.locator.dart com o template
                    content = SETUP_LOCATOR_TEMPLATE.replace("{feature}", feature_name).replace("{Feature}", feature_name.capitalize())
                    create_file(filepath, content)
                elif key == "{feature}.cubit.dart":
                    # Preenche o conteúdo do arquivo de cubit
                    content = CUBIT_TEMPLATE.replace("{feature}", feature_name).replace("{Feature}", feature_name.capitalize())
                    create_file(filepath, content)
                elif key == "{feature}.state.dart":
                    # Preenche o conteúdo do arquivo de state
                    content = STATE_TEMPLATE.replace("{feature}", feature_name).replace("{Feature}", feature_name.capitalize())
                    create_file(filepath, content)
                elif key == "{feature}.page.dart":
                    # Preenche o conteúdo do arquivo de página base
                    content = PAGE_TEMPLATE.replace("{feature}", feature_name).replace("{Feature}", feature_name.capitalize())
                    create_file(filepath, content)
                else:
                    create_file(filepath)  # Cria arquivo vazio



    create_recursive(FEATURE_STRUCTURE, feature_path)

    print(f"Estrutura da feature '{feature_name}' criada em: {feature_path}")


# Caminho base onde a feature será criada
base_directory = input("Digite o caminho base (pasta 'feature' em 'lib'): ").strip()
feature_name = input("Digite o nome da nova feature: ").strip().lower()

if not os.path.exists(base_directory):
    print("O caminho especificado não existe.")
else:
    create_feature_structure(base_directory, feature_name)
