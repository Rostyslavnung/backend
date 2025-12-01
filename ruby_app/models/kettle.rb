require_relative 'base_entity'

class Kettle < BaseEntity
  attr_accessor :model_code, :name, :price, :producer_id, :kettle_type_id, :color_id, :material_id, :capacity, :warranty_months
  attr_accessor :producer_name, :type_name, :color_name, :material_name

  def initialize(id, attrs = {})
    super(id)
    @model_code = attrs[:model_code]
    @name = attrs[:name]
    @price = attrs[:price]
    @producer_id = attrs[:producer_id]
    @kettle_type_id = attrs[:kettle_type_id]
    @color_id = attrs[:color_id]
    @material_id = attrs[:material_id]
    @capacity = attrs[:capacity]
    @warranty_months = attrs[:warranty_months]
    @producer_name = attrs[:producer_name]
    @type_name = attrs[:type_name]
    @color_name = attrs[:color_name]
    @material_name = attrs[:material_name]
  end

  def to_hash
    {
      id: id,
      model_code: model_code,
      name: name,
      price: price,
      producer_id: producer_id,
      kettle_type_id: kettle_type_id,
      color_id: color_id,
      material_id: material_id,
      capacity: capacity,
      warranty_months: warranty_months,
      producer_name: producer_name,
      type_name: type_name,
      color_name: color_name,
      material_name: material_name
    }
  end
end
