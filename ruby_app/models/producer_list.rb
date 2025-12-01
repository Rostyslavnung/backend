require_relative 'base_list'
require_relative 'producer'
require_relative '../config/database'

class ProducerList < BaseList
  def read_from_db
    @items = DB[:producers].order(:id).map do |r|
      Producer.new(r[:id], r[:name])
    end
  end

  def read_from_csv(filename)
    require 'csv'
    CSV.foreach(filename) do |row|
      next if row.empty?
      add(Producer.new(row[0].to_i, row[1]))
    end
  end

  def self.add_to_db(name)
    DB[:producers].insert(name: name)
  end

  def self.update_in_db(id, name)
    DB[:producers].where(id: id).update(name: name)
  end

  def self.delete_from_db(id)
    DB[:producers].where(id: id).delete
  end
end
