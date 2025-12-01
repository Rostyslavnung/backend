require_relative 'base_list'
require_relative 'kettle_type'
require_relative '../config/database'

class KettleTypeList < BaseList
  def read_from_db
    @items = DB[:kettle_types].order(:id).map do |r|
      KettleType.new(r[:id], r[:name])
    end
  end

  def read_from_csv(filename)
    require 'csv'
    CSV.foreach(filename) do |row|
      next if row.empty?
      add(KettleType.new(row[0].to_i, row[1]))
    end
  end

  def self.add_to_db(name)
    DB[:kettle_types].insert(name: name)
  end

  def self.update_in_db(id, name)
    DB[:kettle_types].where(id: id).update(name: name)
  end

  def self.delete_from_db(id)
    DB[:kettle_types].where(id: id).delete
  end
end
