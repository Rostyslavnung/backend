require 'csv'
require_relative 'base_list'
require_relative 'color'
require_relative '../config/database'

class ColorList < BaseList
  def read_from_csv(filename)
    CSV.foreach(filename) do |row|
      next if row.empty?
      id = row[0].to_i
      name = row[1]
      add(Color.new(id, name))
    end
  end

  def get_as_xml
    items_xml = @items.map(&:to_xml).join("\n")
    "<colors>\n#{items_xml}\n</colors>"
  end

  # DB helpers — use Sequel if connected to Postgres/SQLite
  def self.add_to_db(name)
    DB[:colors].insert(name: name)
  rescue Sequel::DatabaseError
    nil
  end

  def self.update_in_db(color_id, name)
    DB[:colors].where(id: color_id).update(name: name)
  rescue Sequel::DatabaseError
    nil
  end

  def self.delete_from_db(color_id)
    DB[:colors].where(id: color_id).delete
  rescue Sequel::DatabaseError
    nil
  end
end
