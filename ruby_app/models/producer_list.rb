require_relative 'base_list'
require_relative 'producer'
require_relative '../config/database'

class ProducerList < BaseList
  def read_from_db
    @items = DB[:producers].order(:id).map do |r|
      Producer.new(r[:id], r[:name])
    end
  end
end
