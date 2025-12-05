require 'sequel'

db_url = ENV['DATABASE_URL']
if db_url.nil? || db_url.to_s.strip.empty?
  raise <<~ERR
    DATABASE_URL is not set. This app is configured to read from Postgres only.
    Set `DATABASE_URL` to a valid Postgres DSN, for example:
      export DATABASE_URL="postgres://user:password@host:5432/database"
  ERR
end

DB = Sequel.connect(db_url, max_connections: 10)

