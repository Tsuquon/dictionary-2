import streamlit as st

# Setup sql database
# conn = st.connection("postgresql", type="sql")
# df = conn.query("SELECT * FROM dictionary LIMIT 1000", ttl='10m')

# for row in df.itertuples():
#     st.write(row)

pg = st.navigation([st.Page("input_chooser.py"), st.Page("flash_card.py")])
pg.run()

