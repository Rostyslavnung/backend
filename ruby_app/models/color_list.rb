require_relative 'base_list'
require_relative 'color'
require_relative '../config/database'

class ColorList < BaseList
  def read_from_db
    @items = DB[:colors].order(:id).map do |r|
      Color.new(r[:id], r[:name])
    end
  end
end
