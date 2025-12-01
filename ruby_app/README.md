# Sinatra + Sequel port (ruby_app)

This folder is a new Sinatra + Sequel Ruby project scaffolded alongside the existing Python app.

Quick start:

1. Install Ruby (3.2+), then install bundler and dependencies:

```bash
gem install bundler
bundle install
```

2. Run the app with Rack: `rackup -p 4567`

By default the app will read CSV files from the repository `data/` directory (same location as the Python app) for simple bootstrapping. To use a database, set `DATABASE_URL` to a PostgreSQL URL or allow the default SQLite file at `ruby_app/db/development.sqlite3`.
