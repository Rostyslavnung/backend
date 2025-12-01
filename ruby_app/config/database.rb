require 'sequel'
require 'csv'
require 'bcrypt'

# seed helper will look for CSV files in the main Python app data folder
data_dir = File.expand_path('../../app/data', __dir__)

# Connect using DATABASE_URL if provided, otherwise fall back to sqlite file
DB = if ENV['DATABASE_URL'] && !ENV['DATABASE_URL'].empty?
  Sequel.connect(ENV['DATABASE_URL'])
else
  db_dir = File.expand_path('../db', __dir__)
  Dir.mkdir(db_dir) unless Dir.exist?(db_dir)
  Sequel.sqlite(File.join(db_dir, 'development.sqlite3'))
end


  # Create minimal tables if they don't exist and seed from CSVs
  DB.create_table? :colors do
    primary_key :id
    String :name
  end

  DB.create_table? :producers do
    primary_key :id
    String :name
  end

  DB.create_table? :materials do
    primary_key :id
    String :name
  end

  DB.create_table? :kettle_types do
    primary_key :id
    String :name
  end

  DB.create_table? :kettles do
    primary_key :id
    String :model_code
    String :name
    Float :price
    Integer :producer_id
    Integer :kettle_type_id
    Integer :color_id
    Integer :material_id
    Float :capacity
    Integer :warranty_months
  end

  def seed_table_from_csv(table_sym, csv_file)
    return unless File.exist?(csv_file)
    table = DB[table_sym]
    return unless table.count == 0
    CSV.foreach(csv_file) do |row|
      next if row.nil? || row.empty?
      # assume first column is id if integer-like
      if row.length >= 2
        id = row[0].to_i
        name = row[1]
        table.insert(id: id, name: name)
      end
    end

    # Users table for authentication
    DB.create_table? :users do
      primary_key :id
      String :username, unique: true, null: false
      String :password_hash, null: false
      TrueClass :is_admin, default: false
    end

    # Seed a default admin user if none exists
    if DB[:users].count == 0
      pw = ENV.fetch('ADMIN_PASSWORD', 'admin')
      pw_hash = BCrypt::Password.create(pw)
      DB[:users].insert(username: 'admin', password_hash: pw_hash.to_s, is_admin: true)
    end
  end

  seed_table_from_csv(:colors, File.join(data_dir, 'colors.csv'))
  seed_table_from_csv(:producers, File.join(data_dir, 'producers.csv'))
  seed_table_from_csv(:materials, File.join(data_dir, 'materials.csv'))
  seed_table_from_csv(:kettle_types, File.join(data_dir, 'kettleTypes.csv'))

  # For kettles.csv we map all columns — skip if table already populated
  kettles_csv = File.join(data_dir, 'kettles.csv')
  if File.exist?(kettles_csv) && DB[:kettles].count == 0
    CSV.foreach(kettles_csv) do |row|
      next if row.nil? || row.empty?
      # expected: id, model_code, name, price, producer_id, kettle_type_id, color_id, material_id, capacity, warranty
      DB[:kettles].insert(
        id: row[0].to_i,
        model_code: row[1].to_s,
        name: row[2].to_s,
        price: (row[3] && row[3] != '') ? row[3].to_f : nil,
        producer_id: (row[4] && row[4] != '') ? row[4].to_i : nil,
        kettle_type_id: (row[5] && row[5] != '') ? row[5].to_i : nil,
        color_id: (row[6] && row[6] != '') ? row[6].to_i : nil,
        material_id: (row[7] && row[7] != '') ? row[7].to_i : nil,
        capacity: (row[8] && row[8] != '') ? row[8].to_f : nil,
        warranty_months: (row[9] && row[9] != '') ? row[9].to_i : nil
      )
    end
  end

