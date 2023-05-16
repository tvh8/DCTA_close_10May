from sqlalchemy import create_engine, inspect

engine = create_engine('sqlite:///site.db')
inspector = inspect(engine)

# Get table information
print(inspector.get_table_names())
