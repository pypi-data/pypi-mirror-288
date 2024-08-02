from typing import Any, Dict

from .base_client import BaseClient
from .get_cube_base_table_name import GetCubeBaseTableName
from .get_cube_name import GetCubeName
from .get_cube_names import GetCubeNames
from .get_dimension_default_hierarchy_name import GetDimensionDefaultHierarchyName
from .get_hierarchy_level_names import GetHierarchyLevelNames
from .get_hierarchy_name import GetHierarchyName
from .get_hierarchy_name_across_dimensions import GetHierarchyNameAcrossDimensions
from .get_hierarchy_names import GetHierarchyNames
from .get_hierarchy_slicing import GetHierarchySlicing
from .get_hierarchy_virtual import GetHierarchyVirtual
from .get_hierarchy_visible import GetHierarchyVisible
from .get_level_name import GetLevelName
from .get_level_name_across_dimensions import GetLevelNameAcrossDimensions
from .get_level_name_across_hierarchies import GetLevelNameAcrossHierarchies
from .get_level_names import GetLevelNames
from .get_table_column_names import GetTableColumnNames
from .get_table_keys import GetTableKeys
from .get_table_name import GetTableName
from .get_table_names import GetTableNames


def gql(q: str) -> str:
    return q


class GraphqlClient(BaseClient):
    def get_cube_base_table_name(
        self, cube_name: str, **kwargs: Any
    ) -> GetCubeBaseTableName:
        query = gql(
            """
            query GetCubeBaseTableName($cubeName: String!) {
              cube(name: $cubeName) {
                baseTable {
                  name
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {"cubeName": cube_name}
        response = self.execute(
            query=query,
            operation_name="GetCubeBaseTableName",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetCubeBaseTableName.model_validate(data)

    def get_cube_name(self, cube_name: str, **kwargs: Any) -> GetCubeName:
        query = gql(
            """
            query GetCubeName($cubeName: String!) {
              cube(name: $cubeName) {
                name
              }
            }
            """
        )
        variables: Dict[str, object] = {"cubeName": cube_name}
        response = self.execute(
            query=query, operation_name="GetCubeName", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetCubeName.model_validate(data)

    def get_cube_names(self, **kwargs: Any) -> GetCubeNames:
        query = gql(
            """
            query GetCubeNames {
              cubes {
                name
              }
            }
            """
        )
        variables: Dict[str, object] = {}
        response = self.execute(
            query=query, operation_name="GetCubeNames", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetCubeNames.model_validate(data)

    def get_dimension_default_hierarchy_name(
        self, cube_name: str, dimension_name: str, **kwargs: Any
    ) -> GetDimensionDefaultHierarchyName:
        query = gql(
            """
            query getDimensionDefaultHierarchyName($cubeName: String!, $dimensionName: String!) {
              cube(name: $cubeName) {
                dimension(name: $dimensionName) {
                  defaultHierarchy {
                    name
                  }
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {
            "cubeName": cube_name,
            "dimensionName": dimension_name,
        }
        response = self.execute(
            query=query,
            operation_name="getDimensionDefaultHierarchyName",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetDimensionDefaultHierarchyName.model_validate(data)

    def get_hierarchy_level_names(
        self, cube_name: str, dimension_name: str, hierarchy_name: str, **kwargs: Any
    ) -> GetHierarchyLevelNames:
        query = gql(
            """
            query GetHierarchyLevelNames($cubeName: String!, $dimensionName: String!, $hierarchyName: String!) {
              cube(name: $cubeName) {
                dimension(name: $dimensionName) {
                  name
                  hierarchy(name: $hierarchyName) {
                    levels {
                      name
                    }
                    name
                    slicing
                  }
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {
            "cubeName": cube_name,
            "dimensionName": dimension_name,
            "hierarchyName": hierarchy_name,
        }
        response = self.execute(
            query=query,
            operation_name="GetHierarchyLevelNames",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetHierarchyLevelNames.model_validate(data)

    def get_hierarchy_name(
        self, cube_name: str, dimension_name: str, hierarchy_name: str, **kwargs: Any
    ) -> GetHierarchyName:
        query = gql(
            """
            query GetHierarchyName($cubeName: String!, $dimensionName: String!, $hierarchyName: String!) {
              cube(name: $cubeName) {
                dimension(name: $dimensionName) {
                  name
                  hierarchy(name: $hierarchyName) {
                    name
                  }
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {
            "cubeName": cube_name,
            "dimensionName": dimension_name,
            "hierarchyName": hierarchy_name,
        }
        response = self.execute(
            query=query,
            operation_name="GetHierarchyName",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetHierarchyName.model_validate(data)

    def get_hierarchy_name_across_dimensions(
        self, cube_name: str, hierarchy_name: str, **kwargs: Any
    ) -> GetHierarchyNameAcrossDimensions:
        query = gql(
            """
            query GetHierarchyNameAcrossDimensions($cubeName: String!, $hierarchyName: String!) {
              cube(name: $cubeName) {
                dimensions {
                  name
                  hierarchy(name: $hierarchyName) {
                    name
                  }
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {
            "cubeName": cube_name,
            "hierarchyName": hierarchy_name,
        }
        response = self.execute(
            query=query,
            operation_name="GetHierarchyNameAcrossDimensions",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetHierarchyNameAcrossDimensions.model_validate(data)

    def get_hierarchy_names(self, cube_name: str, **kwargs: Any) -> GetHierarchyNames:
        query = gql(
            """
            query GetHierarchyNames($cubeName: String!) {
              cube(name: $cubeName) {
                dimensions {
                  name
                  hierarchies {
                    name
                  }
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {"cubeName": cube_name}
        response = self.execute(
            query=query,
            operation_name="GetHierarchyNames",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetHierarchyNames.model_validate(data)

    def get_hierarchy_slicing(
        self, cube_name: str, dimension_name: str, hierarchy_name: str, **kwargs: Any
    ) -> GetHierarchySlicing:
        query = gql(
            """
            query GetHierarchySlicing($cubeName: String!, $dimensionName: String!, $hierarchyName: String!) {
              cube(name: $cubeName) {
                dimension(name: $dimensionName) {
                  name
                  hierarchy(name: $hierarchyName) {
                    slicing
                  }
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {
            "cubeName": cube_name,
            "dimensionName": dimension_name,
            "hierarchyName": hierarchy_name,
        }
        response = self.execute(
            query=query,
            operation_name="GetHierarchySlicing",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetHierarchySlicing.model_validate(data)

    def get_hierarchy_virtual(
        self, cube_name: str, dimension_name: str, hierarchy_name: str, **kwargs: Any
    ) -> GetHierarchyVirtual:
        query = gql(
            """
            query GetHierarchyVirtual($cubeName: String!, $dimensionName: String!, $hierarchyName: String!) {
              cube(name: $cubeName) {
                dimension(name: $dimensionName) {
                  name
                  hierarchy(name: $hierarchyName) {
                    virtual
                  }
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {
            "cubeName": cube_name,
            "dimensionName": dimension_name,
            "hierarchyName": hierarchy_name,
        }
        response = self.execute(
            query=query,
            operation_name="GetHierarchyVirtual",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetHierarchyVirtual.model_validate(data)

    def get_hierarchy_visible(
        self, cube_name: str, dimension_name: str, hierarchy_name: str, **kwargs: Any
    ) -> GetHierarchyVisible:
        query = gql(
            """
            query GetHierarchyVisible($cubeName: String!, $dimensionName: String!, $hierarchyName: String!) {
              cube(name: $cubeName) {
                dimension(name: $dimensionName) {
                  name
                  hierarchy(name: $hierarchyName) {
                    visible
                  }
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {
            "cubeName": cube_name,
            "dimensionName": dimension_name,
            "hierarchyName": hierarchy_name,
        }
        response = self.execute(
            query=query,
            operation_name="GetHierarchyVisible",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetHierarchyVisible.model_validate(data)

    def get_level_name(
        self,
        cube_name: str,
        dimension_name: str,
        hierarchy_name: str,
        level_name: str,
        **kwargs: Any
    ) -> GetLevelName:
        query = gql(
            """
            query GetLevelName($cubeName: String!, $dimensionName: String!, $hierarchyName: String!, $levelName: String!) {
              cube(name: $cubeName) {
                dimension(name: $dimensionName) {
                  name
                  hierarchy(name: $hierarchyName) {
                    level(name: $levelName) {
                      name
                    }
                    name
                  }
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {
            "cubeName": cube_name,
            "dimensionName": dimension_name,
            "hierarchyName": hierarchy_name,
            "levelName": level_name,
        }
        response = self.execute(
            query=query, operation_name="GetLevelName", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetLevelName.model_validate(data)

    def get_level_name_across_dimensions(
        self, cube_name: str, hierarchy_name: str, level_name: str, **kwargs: Any
    ) -> GetLevelNameAcrossDimensions:
        query = gql(
            """
            query GetLevelNameAcrossDimensions($cubeName: String!, $hierarchyName: String!, $levelName: String!) {
              cube(name: $cubeName) {
                dimensions {
                  name
                  hierarchy(name: $hierarchyName) {
                    level(name: $levelName) {
                      name
                    }
                    name
                  }
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {
            "cubeName": cube_name,
            "hierarchyName": hierarchy_name,
            "levelName": level_name,
        }
        response = self.execute(
            query=query,
            operation_name="GetLevelNameAcrossDimensions",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetLevelNameAcrossDimensions.model_validate(data)

    def get_level_name_across_hierarchies(
        self, cube_name: str, level_name: str, **kwargs: Any
    ) -> GetLevelNameAcrossHierarchies:
        query = gql(
            """
            query GetLevelNameAcrossHierarchies($cubeName: String!, $levelName: String!) {
              cube(name: $cubeName) {
                dimensions {
                  name
                  hierarchies {
                    level(name: $levelName) {
                      name
                    }
                    name
                  }
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {"cubeName": cube_name, "levelName": level_name}
        response = self.execute(
            query=query,
            operation_name="GetLevelNameAcrossHierarchies",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetLevelNameAcrossHierarchies.model_validate(data)

    def get_level_names(self, cube_name: str, **kwargs: Any) -> GetLevelNames:
        query = gql(
            """
            query GetLevelNames($cubeName: String!) {
              cube(name: $cubeName) {
                dimensions {
                  name
                  hierarchies {
                    levels {
                      name
                    }
                    name
                    slicing
                  }
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {"cubeName": cube_name}
        response = self.execute(
            query=query, operation_name="GetLevelNames", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetLevelNames.model_validate(data)

    def get_table_column_names(
        self, table_name: str, **kwargs: Any
    ) -> GetTableColumnNames:
        query = gql(
            """
            query GetTableColumnNames($tableName: String!) {
              table(name: $tableName) {
                columns {
                  name
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {"tableName": table_name}
        response = self.execute(
            query=query,
            operation_name="GetTableColumnNames",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetTableColumnNames.model_validate(data)

    def get_table_keys(self, table_name: str, **kwargs: Any) -> GetTableKeys:
        query = gql(
            """
            query GetTableKeys($tableName: String!) {
              table(name: $tableName) {
                columns {
                  name
                }
                keys
              }
            }
            """
        )
        variables: Dict[str, object] = {"tableName": table_name}
        response = self.execute(
            query=query, operation_name="GetTableKeys", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetTableKeys.model_validate(data)

    def get_table_name(self, table_name: str, **kwargs: Any) -> GetTableName:
        query = gql(
            """
            query GetTableName($tableName: String!) {
              table(name: $tableName) {
                name
              }
            }
            """
        )
        variables: Dict[str, object] = {"tableName": table_name}
        response = self.execute(
            query=query, operation_name="GetTableName", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetTableName.model_validate(data)

    def get_table_names(self, **kwargs: Any) -> GetTableNames:
        query = gql(
            """
            query GetTableNames {
              tables {
                name
              }
            }
            """
        )
        variables: Dict[str, object] = {}
        response = self.execute(
            query=query, operation_name="GetTableNames", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetTableNames.model_validate(data)
