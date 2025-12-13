require_relative 'base_list'
require_relative 'kettle'
require_relative '../config/database'

class KettleList < BaseList
  def read_from_db()
    pk = Sequel.qualify(:kettles, :id)
    select_cols = [
      Sequel.qualify(:kettles, :id).as(:id),
      Sequel.qualify(:kettles, :model_code).as(:model_code),
      Sequel.qualify(:kettles, :name).as(:name),
      Sequel.qualify(:kettles, :price).as(:price),
      Sequel.qualify(:kettles, :producer_id).as(:producer_id),
      Sequel.qualify(:kettles, :kettle_type_id).as(:kettle_type_id),
      Sequel.qualify(:kettles, :color_id).as(:color_id),
      Sequel.qualify(:kettles, :material_id).as(:material_id),
      Sequel.qualify(:kettles, :capacity).as(:capacity),
      Sequel.qualify(:kettles, :warranty_months).as(:warranty_months),
      Sequel.qualify(:producers, :name).as(:producer_name),
      Sequel.qualify(:kettle_types, :name).as(:type_name),
      Sequel.qualify(:colors, :name).as(:color_name),
      Sequel.qualify(:materials, :name).as(:material_name)
    ]

        ds = DB[:kettles]
          .select(*select_cols)
          .left_join(:producers, Sequel[:producers][:id] => Sequel[:kettles][:producer_id])
          .left_join(:kettle_types, Sequel[:kettle_types][:id] => Sequel[:kettles][:kettle_type_id])
          .left_join(:colors, Sequel[:colors][:id] => Sequel[:kettles][:color_id])
          .left_join(:materials, Sequel[:materials][:id] => Sequel[:kettles][:material_id])

    @items = ds.all.map do |r|
      Kettle.new(r[:id],
                 model_code: r[:model_code], name: r[:name], price: r[:price].to_f,
                 producer_id: r[:producer_id], kettle_type_id: r[:kettle_type_id],
                 color_id: r[:color_id], material_id: r[:material_id],
                 capacity: r[:capacity].to_f, warranty_months: r[:warranty_months],
                 producer_name: r[:producer_name], type_name: r[:type_name],
                 color_name: r[:color_name], material_name: r[:material_name])
    end
  end
end
