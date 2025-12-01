require_relative 'base_list'
require_relative 'material'
require_relative '../config/database'

class MaterialList < BaseList
  def read_from_db
    @items = DB[:materials].order(:id).map do |r|
      Material.new(r[:id], r[:name])
    end
  end

  def read_from_csv(filename)
    require 'csv'
    CSV.foreach(filename) do |row|
      next if row.empty?
      add(Material.new(row[0].to_i, row[1]))
    end
  end

  def self.add_to_db(name)
    DB[:materials].insert(name: name)
  end

  def self.update_in_db(id, name)
    DB[:materials].where(id: id).update(name: name)
  end

  def self.delete_from_db(id)
    DB[:materials].where(id: id).delete
  end
end
