import requests
import time
import os

DIRECTUS_HOST = os.environ.get("DIRECTUS_HOST", "http://localhost:8055")
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@example.com")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "password")


def main():

    polling = True

    while polling:
        try:
            print("Polling directus...")
            response = requests.post(
                f"{DIRECTUS_HOST}/auth/login",
                json={
                    "email": ADMIN_EMAIL, 
                    "password": ADMIN_PASSWORD,
                }
            )
            if response.status_code != 200:
                raise AssertionError            
            admin_access_token = response.json()["data"]["access_token"]
            polling = False
        except Exception:
            time.sleep(1.0)

    # create ai_rag_feedback table with fields
    print("Creating ai_rag_feedback table...")
    requests.post(
        f"{DIRECTUS_HOST}/collections",
        headers={
            "Authorization": f"Bearer {admin_access_token}",
        },
        json={
            "collection": "ai_rag_feedback",
            "meta": {
            "collection": "ai_rag_feedback",
            "icon": None,
            "note": None,
            "display_template": None,
            "hidden": False,
            "singleton": False,
            "translations": None,
            "archive_field": None,
            "archive_app_filter": True,
            "archive_value": None,
            "unarchive_value": None,
            "sort_field": None,
            "accountability": "all",
            "color": None,
            "item_duplication_fields": None,
            "sort": None,
            "group": None,
            "collapse": "open",
            "preview_url": None,
            "versioning": False
            },
            "schema": {
            "name": "ai_rag_feedback",
            "sql": "CREATE TABLE \"ai_rag_feedback\" (`id` integer PRIMARY KEY AUTOINCREMENT NOT None, `user_created` char(36) None, `date_created` datetime None, `user_updated` char(36) None, `date_updated` datetime None, `query` text None, `rag_response` text None, `score` float None, `comments` text None, CONSTRAINT `ai_rag_feedback_user_created_foreign` FOREIGN KEY (`user_created`) REFERENCES `directus_users` (`id`), CONSTRAINT `ai_rag_feedback_user_updated_foreign` FOREIGN KEY (`user_updated`) REFERENCES `directus_users` (`id`))"
            },
            "fields": [
                {
                    "collection": "ai_rag_feedback",
                    "field": "id",
                    "type": "integer",
                    "schema": {
                        "name": "id",
                        "table": "ai_rag_feedback",
                        "data_type": "integer",
                        "default_value": None,
                        "max_length": None,
                        "numeric_precision": None,
                        "numeric_scale": None,
                        "is_generated": False,
                        "generation_expression": None,
                        "is_Noneable": False,
                        "is_unique": False,
                        "is_primary_key": True,
                        "has_auto_increment": True,
                        "foreign_key_column": None,
                        "foreign_key_table": None
                    },
                    "meta": {
                        "id": 17,
                        "collection": "ai_rag_feedback",
                        "field": "id",
                        "special": None,
                        "interface": "input",
                        "options": None,
                        "display": None,
                        "display_options": None,
                        "readonly": True,
                        "hidden": True,
                        "sort": 1,
                        "width": "full",
                        "translations": None,
                        "note": None,
                        "conditions": None,
                        "required": False,
                        "group": None,
                        "validation": None,
                        "validation_message": None
                    }
                },
                {
                    "collection": "ai_rag_feedback",
                    "field": "user_created",
                    "type": "string",
                    "schema": {
                        "name": "user_created",
                        "table": "ai_rag_feedback",
                        "data_type": "char",
                        "default_value": None,
                        "max_length": 36,
                        "numeric_precision": None,
                        "numeric_scale": None,
                        "is_generated": False,
                        "generation_expression": None,
                        "is_Noneable": True,
                        "is_unique": False,
                        "is_primary_key": False,
                        "has_auto_increment": False,
                        "foreign_key_column": "id",
                        "foreign_key_table": "directus_users"
                    },
                    "meta": {
                        "id": 18,
                        "collection": "ai_rag_feedback",
                        "field": "user_created",
                        "special": [
                        "user-created"
                        ],
                        "interface": "select-dropdown-m2o",
                        "options": {
                        "template": "{{avatar.$thumbnail}} {{first_name}} {{last_name}}"
                        },
                        "display": "user",
                        "display_options": None,
                        "readonly": True,
                        "hidden": True,
                        "sort": 2,
                        "width": "half",
                        "translations": None,
                        "note": None,
                        "conditions": None,
                        "required": False,
                        "group": None,
                        "validation": None,
                        "validation_message": None
                    }
                },
                {
                    "collection": "ai_rag_feedback",
                    "field": "date_created",
                    "type": "timestamp",
                    "schema": {
                        "name": "date_created",
                        "table": "ai_rag_feedback",
                        "data_type": "datetime",
                        "default_value": None,
                        "max_length": None,
                        "numeric_precision": None,
                        "numeric_scale": None,
                        "is_generated": False,
                        "generation_expression": None,
                        "is_Noneable": True,
                        "is_unique": False,
                        "is_primary_key": False,
                        "has_auto_increment": False,
                        "foreign_key_column": None,
                        "foreign_key_table": None
                    },
                    "meta": {
                        "id": 19,
                        "collection": "ai_rag_feedback",
                        "field": "date_created",
                        "special": [
                        "date-created",
                        "cast-timestamp"
                        ],
                        "interface": "datetime",
                        "options": None,
                        "display": "datetime",
                        "display_options": {
                        "relative": True
                        },
                        "readonly": True,
                        "hidden": True,
                        "sort": 3,
                        "width": "half",
                        "translations": None,
                        "note": None,
                        "conditions": None,
                        "required": False,
                        "group": None,
                        "validation": None,
                        "validation_message": None
                    }
                },
                {
                    "collection": "ai_rag_feedback",
                    "field": "user_updated",
                    "type": "string",
                    "schema": {
                        "name": "user_updated",
                        "table": "ai_rag_feedback",
                        "data_type": "char",
                        "default_value": None,
                        "max_length": 36,
                        "numeric_precision": None,
                        "numeric_scale": None,
                        "is_generated": False,
                        "generation_expression": None,
                        "is_Noneable": True,
                        "is_unique": False,
                        "is_primary_key": False,
                        "has_auto_increment": False,
                        "foreign_key_column": "id",
                        "foreign_key_table": "directus_users"
                    },
                    "meta": {
                        "id": 20,
                        "collection": "ai_rag_feedback",
                        "field": "user_updated",
                        "special": [
                        "user-updated"
                        ],
                        "interface": "select-dropdown-m2o",
                        "options": {
                        "template": "{{avatar.$thumbnail}} {{first_name}} {{last_name}}"
                        },
                        "display": "user",
                        "display_options": None,
                        "readonly": True,
                        "hidden": True,
                        "sort": 4,
                        "width": "half",
                        "translations": None,
                        "note": None,
                        "conditions": None,
                        "required": False,
                        "group": None,
                        "validation": None,
                        "validation_message": None
                    }
                },
                {
                    "collection": "ai_rag_feedback",
                    "field": "date_updated",
                    "type": "timestamp",
                    "schema": {
                        "name": "date_updated",
                        "table": "ai_rag_feedback",
                        "data_type": "datetime",
                        "default_value": None,
                        "max_length": None,
                        "numeric_precision": None,
                        "numeric_scale": None,
                        "is_generated": False,
                        "generation_expression": None,
                        "is_Noneable": True,
                        "is_unique": False,
                        "is_primary_key": False,
                        "has_auto_increment": False,
                        "foreign_key_column": None,
                        "foreign_key_table": None
                    },
                    "meta": {
                        "id": 21,
                        "collection": "ai_rag_feedback",
                        "field": "date_updated",
                        "special": [
                        "date-updated",
                        "cast-timestamp"
                        ],
                        "interface": "datetime",
                        "options": None,
                        "display": "datetime",
                        "display_options": {
                        "relative": True
                        },
                        "readonly": True,
                        "hidden": True,
                        "sort": 5,
                        "width": "half",
                        "translations": None,
                        "note": None,
                        "conditions": None,
                        "required": False,
                        "group": None,
                        "validation": None,
                        "validation_message": None
                    }
                },
                {
                    "collection": "ai_rag_feedback",
                    "field": "query",
                    "type": "text",
                    "schema": {
                        "name": "query",
                        "table": "ai_rag_feedback",
                        "data_type": "text",
                        "default_value": None,
                        "max_length": None,
                        "numeric_precision": None,
                        "numeric_scale": None,
                        "is_generated": False,
                        "generation_expression": None,
                        "is_Noneable": True,
                        "is_unique": False,
                        "is_primary_key": False,
                        "has_auto_increment": False,
                        "foreign_key_column": None,
                        "foreign_key_table": None
                    },
                    "meta": {
                        "id": 22,
                        "collection": "ai_rag_feedback",
                        "field": "query",
                        "special": None,
                        "interface": "input",
                        "options": None,
                        "display": None,
                        "display_options": None,
                        "readonly": False,
                        "hidden": False,
                        "sort": 6,
                        "width": "full",
                        "translations": None,
                        "note": None,
                        "conditions": None,
                        "required": True,
                        "group": None,
                        "validation": None,
                        "validation_message": None
                    }
                },
                {
                    "collection": "ai_rag_feedback",
                    "field": "rag_response",
                    "type": "text",
                    "schema": {
                        "name": "rag_response",
                        "table": "ai_rag_feedback",
                        "data_type": "text",
                        "default_value": None,
                        "max_length": None,
                        "numeric_precision": None,
                        "numeric_scale": None,
                        "is_generated": False,
                        "generation_expression": None,
                        "is_Noneable": True,
                        "is_unique": False,
                        "is_primary_key": False,
                        "has_auto_increment": False,
                        "foreign_key_column": None,
                        "foreign_key_table": None
                    },
                    "meta": {
                        "id": 23,
                        "collection": "ai_rag_feedback",
                        "field": "rag_response",
                        "special": None,
                        "interface": "input",
                        "options": None,
                        "display": None,
                        "display_options": None,
                        "readonly": False,
                        "hidden": False,
                        "sort": 7,
                        "width": "full",
                        "translations": None,
                        "note": None,
                        "conditions": None,
                        "required": True,
                        "group": None,
                        "validation": None,
                        "validation_message": None
                    }
                },
                {
                    "collection": "ai_rag_feedback",
                    "field": "score",
                    "type": "float",
                    "schema": {
                        "name": "score",
                        "table": "ai_rag_feedback",
                        "data_type": "float",
                        "default_value": None,
                        "max_length": None,
                        "numeric_precision": None,
                        "numeric_scale": None,
                        "is_generated": False,
                        "generation_expression": None,
                        "is_Noneable": True,
                        "is_unique": False,
                        "is_primary_key": False,
                        "has_auto_increment": False,
                        "foreign_key_column": None,
                        "foreign_key_table": None
                    },
                    "meta": {
                        "id": 24,
                        "collection": "ai_rag_feedback",
                        "field": "score",
                        "special": None,
                        "interface": "select-dropdown",
                        "options": {
                        "choices": [
                            {
                            "text": "😀",
                            "value": 1
                            },
                            {
                            "text": "🙂",
                            "value": 0.75
                            },
                            {
                            "text": "😐",
                            "value": 0.5
                            },
                            {
                            "text": "🙁",
                            "value": 0.25
                            },
                            {
                            "text": "😞",
                            "value": 0
                            }
                        ]
                        },
                        "display": None,
                        "display_options": None,
                        "readonly": False,
                        "hidden": False,
                        "sort": 8,
                        "width": "full",
                        "translations": None,
                        "note": None,
                        "conditions": None,
                        "required": True,
                        "group": None,
                        "validation": None,
                        "validation_message": None
                    }
                },
                {
                    "collection": "ai_rag_feedback",
                    "field": "comments",
                    "type": "text",
                    "schema": {
                        "name": "comments",
                        "table": "ai_rag_feedback",
                        "data_type": "text",
                        "default_value": None,
                        "max_length": None,
                        "numeric_precision": None,
                        "numeric_scale": None,
                        "is_generated": False,
                        "generation_expression": None,
                        "is_Noneable": True,
                        "is_unique": False,
                        "is_primary_key": False,
                        "has_auto_increment": False,
                        "foreign_key_column": None,
                        "foreign_key_table": None
                    },
                    "meta": {
                        "id": 25,
                        "collection": "ai_rag_feedback",
                        "field": "comments",
                        "special": None,
                        "interface": "input",
                        "options": None,
                        "display": None,
                        "display_options": None,
                        "readonly": False,
                        "hidden": False,
                        "sort": 9,
                        "width": "full",
                        "translations": None,
                        "note": None,
                        "conditions": None,
                        "required": False,
                        "group": None,
                        "validation": None,
                        "validation_message": None
                    }
                }
            ]
        }
    )

    # create ai_search_feedback table with fields
    print("Creating ai_search_feedback table...")
    requests.post(
        f"{DIRECTUS_HOST}/collections",
        headers={
            "Authorization": f"Bearer {admin_access_token}",
        },
        json={
            "collection": "ai_search_feedback",
            "meta": {
            "collection": "ai_search_feedback",
            "icon": None,
            "note": None,
            "display_template": None,
            "hidden": False,
            "singleton": False,
            "translations": None,
            "archive_field": None,
            "archive_app_filter": True,
            "archive_value": None,
            "unarchive_value": None,
            "sort_field": None,
            "accountability": "all",
            "color": None,
            "item_duplication_fields": None,
            "sort": None,
            "group": None,
            "collapse": "open",
            "preview_url": None,
            "versioning": False
            },
            "schema": {
            "name": "ai_search_feedback",
            "sql": "CREATE TABLE \"ai_search_feedback\" (`id` integer PRIMARY KEY AUTOINCREMENT NOT None, `user_created` char(36) None, `date_created` datetime None, `user_updated` char(36) None, `date_updated` datetime None, `query` text None, `page_content` text None, `title` text None, `link` text None, `score` float None, `comments` text None, CONSTRAINT `ai_search_feedback_user_created_foreign` FOREIGN KEY (`user_created`) REFERENCES `directus_users` (`id`), CONSTRAINT `ai_search_feedback_user_updated_foreign` FOREIGN KEY (`user_updated`) REFERENCES `directus_users` (`id`))"
            },
            "fields": [
                {
                "collection": "ai_search_feedback",
                "field": "id",
                "type": "integer",
                "schema": {
                    "name": "id",
                    "table": "ai_search_feedback",
                    "data_type": "integer",
                    "default_value": None,
                    "max_length": None,
                    "numeric_precision": None,
                    "numeric_scale": None,
                    "is_generated": False,
                    "generation_expression": None,
                    "is_Noneable": False,
                    "is_unique": False,
                    "is_primary_key": True,
                    "has_auto_increment": True,
                    "foreign_key_column": None,
                    "foreign_key_table": None
                },
                "meta": {
                    "id": 2,
                    "collection": "ai_search_feedback",
                    "field": "id",
                    "special": None,
                    "interface": "input",
                    "options": None,
                    "display": None,
                    "display_options": None,
                    "readonly": True,
                    "hidden": True,
                    "sort": 1,
                    "width": "full",
                    "translations": None,
                    "note": None,
                    "conditions": None,
                    "required": False,
                    "group": None,
                    "validation": None,
                    "validation_message": None
                }
                },
                {
                "collection": "ai_search_feedback",
                "field": "user_created",
                "type": "string",
                "schema": {
                    "name": "user_created",
                    "table": "ai_search_feedback",
                    "data_type": "char",
                    "default_value": None,
                    "max_length": 36,
                    "numeric_precision": None,
                    "numeric_scale": None,
                    "is_generated": False,
                    "generation_expression": None,
                    "is_Noneable": True,
                    "is_unique": False,
                    "is_primary_key": False,
                    "has_auto_increment": False,
                    "foreign_key_column": "id",
                    "foreign_key_table": "directus_users"
                },
                "meta": {
                    "id": 3,
                    "collection": "ai_search_feedback",
                    "field": "user_created",
                    "special": [
                    "user-created"
                    ],
                    "interface": "select-dropdown-m2o",
                    "options": {
                    "template": "{{avatar.$thumbnail}} {{first_name}} {{last_name}}"
                    },
                    "display": "user",
                    "display_options": None,
                    "readonly": True,
                    "hidden": True,
                    "sort": 2,
                    "width": "half",
                    "translations": None,
                    "note": None,
                    "conditions": None,
                    "required": False,
                    "group": None,
                    "validation": None,
                    "validation_message": None
                }
                },
                {
                "collection": "ai_search_feedback",
                "field": "date_created",
                "type": "timestamp",
                "schema": {
                    "name": "date_created",
                    "table": "ai_search_feedback",
                    "data_type": "datetime",
                    "default_value": None,
                    "max_length": None,
                    "numeric_precision": None,
                    "numeric_scale": None,
                    "is_generated": False,
                    "generation_expression": None,
                    "is_Noneable": True,
                    "is_unique": False,
                    "is_primary_key": False,
                    "has_auto_increment": False,
                    "foreign_key_column": None,
                    "foreign_key_table": None
                },
                "meta": {
                    "id": 4,
                    "collection": "ai_search_feedback",
                    "field": "date_created",
                    "special": [
                    "date-created",
                    "cast-timestamp"
                    ],
                    "interface": "datetime",
                    "options": None,
                    "display": "datetime",
                    "display_options": {
                    "relative": True
                    },
                    "readonly": True,
                    "hidden": True,
                    "sort": 3,
                    "width": "half",
                    "translations": None,
                    "note": None,
                    "conditions": None,
                    "required": False,
                    "group": None,
                    "validation": None,
                    "validation_message": None
                }
                },
                {
                "collection": "ai_search_feedback",
                "field": "user_updated",
                "type": "string",
                "schema": {
                    "name": "user_updated",
                    "table": "ai_search_feedback",
                    "data_type": "char",
                    "default_value": None,
                    "max_length": 36,
                    "numeric_precision": None,
                    "numeric_scale": None,
                    "is_generated": False,
                    "generation_expression": None,
                    "is_Noneable": True,
                    "is_unique": False,
                    "is_primary_key": False,
                    "has_auto_increment": False,
                    "foreign_key_column": "id",
                    "foreign_key_table": "directus_users"
                },
                "meta": {
                    "id": 5,
                    "collection": "ai_search_feedback",
                    "field": "user_updated",
                    "special": [
                    "user-updated"
                    ],
                    "interface": "select-dropdown-m2o",
                    "options": {
                    "template": "{{avatar.$thumbnail}} {{first_name}} {{last_name}}"
                    },
                    "display": "user",
                    "display_options": None,
                    "readonly": True,
                    "hidden": True,
                    "sort": 4,
                    "width": "half",
                    "translations": None,
                    "note": None,
                    "conditions": None,
                    "required": False,
                    "group": None,
                    "validation": None,
                    "validation_message": None
                }
                },
                {
                "collection": "ai_search_feedback",
                "field": "date_updated",
                "type": "timestamp",
                "schema": {
                    "name": "date_updated",
                    "table": "ai_search_feedback",
                    "data_type": "datetime",
                    "default_value": None,
                    "max_length": None,
                    "numeric_precision": None,
                    "numeric_scale": None,
                    "is_generated": False,
                    "generation_expression": None,
                    "is_Noneable": True,
                    "is_unique": False,
                    "is_primary_key": False,
                    "has_auto_increment": False,
                    "foreign_key_column": None,
                    "foreign_key_table": None
                },
                "meta": {
                    "id": 6,
                    "collection": "ai_search_feedback",
                    "field": "date_updated",
                    "special": [
                    "date-updated",
                    "cast-timestamp"
                    ],
                    "interface": "datetime",
                    "options": None,
                    "display": "datetime",
                    "display_options": {
                    "relative": True
                    },
                    "readonly": True,
                    "hidden": True,
                    "sort": 5,
                    "width": "half",
                    "translations": None,
                    "note": None,
                    "conditions": None,
                    "required": False,
                    "group": None,
                    "validation": None,
                    "validation_message": None
                }
                },
                {
                "collection": "ai_search_feedback",
                "field": "query",
                "type": "text",
                "schema": {
                    "name": "query",
                    "table": "ai_search_feedback",
                    "data_type": "text",
                    "default_value": None,
                    "max_length": None,
                    "numeric_precision": None,
                    "numeric_scale": None,
                    "is_generated": False,
                    "generation_expression": None,
                    "is_Noneable": True,
                    "is_unique": False,
                    "is_primary_key": False,
                    "has_auto_increment": False,
                    "foreign_key_column": None,
                    "foreign_key_table": None
                },
                "meta": {
                    "id": 8,
                    "collection": "ai_search_feedback",
                    "field": "query",
                    "special": None,
                    "interface": "input",
                    "options": None,
                    "display": None,
                    "display_options": None,
                    "readonly": False,
                    "hidden": False,
                    "sort": 6,
                    "width": "full",
                    "translations": None,
                    "note": None,
                    "conditions": None,
                    "required": False,
                    "group": None,
                    "validation": None,
                    "validation_message": None
                }
                },
                {
                "collection": "ai_search_feedback",
                "field": "page_content",
                "type": "text",
                "schema": {
                    "name": "page_content",
                    "table": "ai_search_feedback",
                    "data_type": "text",
                    "default_value": None,
                    "max_length": None,
                    "numeric_precision": None,
                    "numeric_scale": None,
                    "is_generated": False,
                    "generation_expression": None,
                    "is_Noneable": True,
                    "is_unique": False,
                    "is_primary_key": False,
                    "has_auto_increment": False,
                    "foreign_key_column": None,
                    "foreign_key_table": None
                },
                "meta": {
                    "id": 11,
                    "collection": "ai_search_feedback",
                    "field": "page_content",
                    "special": None,
                    "interface": "input",
                    "options": None,
                    "display": None,
                    "display_options": None,
                    "readonly": False,
                    "hidden": False,
                    "sort": 7,
                    "width": "full",
                    "translations": None,
                    "note": None,
                    "conditions": None,
                    "required": False,
                    "group": None,
                    "validation": None,
                    "validation_message": None
                }
                },
                {
                "collection": "ai_search_feedback",
                "field": "title",
                "type": "text",
                "schema": {
                    "name": "title",
                    "table": "ai_search_feedback",
                    "data_type": "text",
                    "default_value": None,
                    "max_length": None,
                    "numeric_precision": None,
                    "numeric_scale": None,
                    "is_generated": False,
                    "generation_expression": None,
                    "is_Noneable": True,
                    "is_unique": False,
                    "is_primary_key": False,
                    "has_auto_increment": False,
                    "foreign_key_column": None,
                    "foreign_key_table": None
                },
                "meta": {
                    "id": 12,
                    "collection": "ai_search_feedback",
                    "field": "title",
                    "special": None,
                    "interface": "input",
                    "options": None,
                    "display": None,
                    "display_options": None,
                    "readonly": False,
                    "hidden": False,
                    "sort": 8,
                    "width": "full",
                    "translations": None,
                    "note": None,
                    "conditions": None,
                    "required": False,
                    "group": None,
                    "validation": None,
                    "validation_message": None
                }
                },
                {
                "collection": "ai_search_feedback",
                "field": "link",
                "type": "text",
                "schema": {
                    "name": "link",
                    "table": "ai_search_feedback",
                    "data_type": "text",
                    "default_value": None,
                    "max_length": None,
                    "numeric_precision": None,
                    "numeric_scale": None,
                    "is_generated": False,
                    "generation_expression": None,
                    "is_Noneable": True,
                    "is_unique": False,
                    "is_primary_key": False,
                    "has_auto_increment": False,
                    "foreign_key_column": None,
                    "foreign_key_table": None
                },
                "meta": {
                    "id": 13,
                    "collection": "ai_search_feedback",
                    "field": "link",
                    "special": None,
                    "interface": "input",
                    "options": None,
                    "display": None,
                    "display_options": None,
                    "readonly": False,
                    "hidden": False,
                    "sort": 9,
                    "width": "full",
                    "translations": None,
                    "note": None,
                    "conditions": None,
                    "required": False,
                    "group": None,
                    "validation": None,
                    "validation_message": None
                }
                },
                {
                "collection": "ai_search_feedback",
                "field": "score",
                "type": "float",
                "schema": {
                    "name": "score",
                    "table": "ai_search_feedback",
                    "data_type": "float",
                    "default_value": None,
                    "max_length": None,
                    "numeric_precision": None,
                    "numeric_scale": None,
                    "is_generated": False,
                    "generation_expression": None,
                    "is_Noneable": True,
                    "is_unique": False,
                    "is_primary_key": False,
                    "has_auto_increment": False,
                    "foreign_key_column": None,
                    "foreign_key_table": None
                },
                "meta": {
                    "id": 15,
                    "collection": "ai_search_feedback",
                    "field": "score",
                    "special": None,
                    "interface": "select-dropdown",
                    "options": {
                    "choices": [
                        {
                        "text": "😀",
                        "value": 1
                        },
                        {
                        "text": "🙂",
                        "value": 0.75
                        },
                        {
                        "text": "😐",
                        "value": 0.5
                        },
                        {
                        "text": "🙁",
                        "value": 0.25
                        },
                        {
                        "text": "😞",
                        "value": 0
                        }
                    ]
                    },
                    "display": None,
                    "display_options": None,
                    "readonly": False,
                    "hidden": False,
                    "sort": 10,
                    "width": "full",
                    "translations": None,
                    "note": None,
                    "conditions": None,
                    "required": True,
                    "group": None,
                    "validation": None,
                    "validation_message": None
                }
                },
                {
                "collection": "ai_search_feedback",
                "field": "comments",
                "type": "text",
                "schema": {
                    "name": "comments",
                    "table": "ai_search_feedback",
                    "data_type": "text",
                    "default_value": None,
                    "max_length": None,
                    "numeric_precision": None,
                    "numeric_scale": None,
                    "is_generated": False,
                    "generation_expression": None,
                    "is_Noneable": True,
                    "is_unique": False,
                    "is_primary_key": False,
                    "has_auto_increment": False,
                    "foreign_key_column": None,
                    "foreign_key_table": None
                },
                "meta": {
                    "id": 16,
                    "collection": "ai_search_feedback",
                    "field": "comments",
                    "special": None,
                    "interface": "input",
                    "options": None,
                    "display": None,
                    "display_options": None,
                    "readonly": False,
                    "hidden": False,
                    "sort": 11,
                    "width": "full",
                    "translations": None,
                    "note": None,
                    "conditions": None,
                    "required": False,
                    "group": None,
                    "validation": None,
                    "validation_message": None
                }
                }
            ]
        }
    )

    # Set admin access token
    print("Setting admin access token...")
    requests.patch(
        f"{DIRECTUS_HOST}/users/me",
        headers={
            "Authorization": f"Bearer {admin_access_token}",
        },
        json={
            "token": "btFBH6DZzvhfufNYakQOmozszmFtEByj"
        }
    )

if __name__ == "__main__":
    main()
