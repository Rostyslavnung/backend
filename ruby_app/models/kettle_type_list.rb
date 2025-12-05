require_relative 'base_list'
require_relative 'kettle_type'
require_relative '../config/database'

class KettleTypeList < BaseList
  def read_from_db
    @items = DB[:kettle_types].order(:id).map do |r|
      KettleType.new(r[:id], r[:name])
    end
  end
end
