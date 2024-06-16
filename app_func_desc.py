func_desc = [
            {
                "name": "execute_query",
                "description": "Execute a query against a database or a predefined service and return the result.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "modified_question": {
                            "type": "string",
                            "description": "modified question considering database structure that suggests what data should be extracted from database to answer the user's question. Example: Question: How many questions are asked by Ed and list all the questions?\n modified_question: Can you count and list all the entries where the 'userName' field is 'Macnamara, Ed' and extract the corresponding 'userQuestion' fields?"
                        },
                        "database_query": {
                            "type": "string",
                            "description": "The query string used to query the database or service."
                        }
                    },
                    "required": ["modified_question", "database_query"],
                    "description": "The input parameters consisting of user-provided query and database query."
                },
                "returns": {
                    "type": "string",
                    "description": "A string representation of the query result. The result can be obtained from the database or a service response."
                }
            },
            {
                "name": "get_power_user",
                "description": "Retrieve data from a database within a specified date range and process it to identify power users based on question activity.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "A user's query parameter"
                        }
                    },
                    "required": ["query"],
                    "description": "The input parameter (not used in the function logic but serves as an input placeholder)."
                },
                "returns": {
                    "type": "string",
                    "description": "A string representation of a DataFrame containing aggregated question counts grouped by user email, identifying power users."
                }
            }
        ]