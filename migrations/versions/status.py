from alembic import op
import sqlalchemy as sa

# Rename the table if necessary
def upgrade():
    # SQLite doesn't support dropping constraints directly, so we have to recreate the table
    # Step 1: Create a new temporary table without the unique constraint
    op.create_table('customer_temp',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=100), nullable=True),  # No unique constraint here
        # Add other columns here, as needed, to match the original 'customer' table
        sa.PrimaryKeyConstraint('id')
    )

    # Step 2: Copy data from the old table to the new temporary table
    op.execute('INSERT INTO customer_temp (id, status) SELECT id, status FROM customer')

    # Step 3: Drop the old table
    op.drop_table('customer')

    # Step 4: Rename the new table to the original table name
    op.rename_table('customer_temp', 'customer')


