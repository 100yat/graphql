from strawberry.fastapi import GraphQLRouter
from strawberry.tools import merge_types
from strawberry import Schema
from src.user.userView import UserQuery
from src.transaction.transactionView import TransactionQuery
from src.balance.balanceView import BalanceQuery

schema = Schema(query=merge_types("Query", (UserQuery, TransactionQuery, BalanceQuery)))

graphql_app = GraphQLRouter(schema)  # graphiql=False