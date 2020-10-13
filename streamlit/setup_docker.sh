mkdir -p ~/.streamlit/

echo -e "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = 8502\n\
" > ~/.streamlit/config.toml
