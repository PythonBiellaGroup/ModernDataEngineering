export PYTHONPATH=$(pwd)
export VERBOSITY=DEBUG
streamlit run app/main.py --server.port=8081
#python3 app/main.py