if [[ -z "$VIRTUAL_ENV" ]]; then
    source venv/bin/activate
else
    echo "VIRTUAL_ENV is already set"
fi

flask --app main run --host=0.0.0.0 --port=8081 --debug