require_relative 'base_list'
require_relative 'material'
require_relative '../config/database'

class MaterialList < BaseList
  def read_from_db
    @items = DB[:materials].order(:id).map do |r|
      Material.new(r[:id], r[:name])
    end
  end
end
