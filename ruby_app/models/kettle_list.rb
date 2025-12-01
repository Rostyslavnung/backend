require_relative 'base_list'
require_relative 'kettle'
require_relative '../config/database'

class KettleList < BaseList
  # load kettles with joined names for related entities
  def read_from_db(filters = {})
    ds = DB[:kettles]
            .left_join(:producers, id: :producer_id)
            .left_join(:kettle_types, id: :kettle_type_id)
            .left_join(:colors, id: :color_id)
            .left_join(:materials, id: :material_id)
            .select_all(:kettles)
            .select_append(Sequel[:producers][:name].as(:producer_name))
            .select_append(Sequel[:kettle_types][:name].as(:type_name))
            .select_append(Sequel[:colors][:name].as(:color_name))
            .select_append(Sequel[:materials][:name].as(:material_name))

    if filters[:q]
      q = "%#{filters[:q]}%"
      ds = ds.where(Sequel.ilike(:kettles__name, q))
    end
    if filters[:producer]
      ds = ds.where(producer_id: filters[:producer].to_i)
    end
    if filters[:sort]
      ds = ds.order(filters[:sort].to_sym)
    else
      ds = ds.order(:id)
    end

    @items = ds.map do |r|
      Kettle.new(r[:id],
                 model_code: r[:model_code], name: r[:name], price: r[:price],
                 producer_id: r[:producer_id], kettle_type_id: r[:kettle_type_id],
                 color_id: r[:color_id], material_id: r[:material_id],
                 capacity: r[:capacity], warranty_months: r[:warranty_months],
                 producer_name: r[:producer_name], type_name: r[:type_name],
                 color_name: r[:color_name], material_name: r[:material_name])
    end
  end

  def read_from_csv(filename)
    require 'csv'
    CSV.foreach(filename) do |row|
      next if row.empty?
      add(Kettle.new(row[0].to_i, model_code: row[1], name: row[2], price: (row[3] && row[3] != '') ? row[3].to_f : nil,
                     producer_id: (row[4] && row[4] != '') ? row[4].to_i : nil,
                     kettle_type_id: (row[5] && row[5] != '') ? row[5].to_i : nil,
                     color_id: (row[6] && row[6] != '') ? row[6].to_i : nil,
                     material_id: (row[7] && row[7] != '') ? row[7].to_i : nil,
                     capacity: (row[8] && row[8] != '') ? row[8].to_f : nil,
                     warranty_months: (row[9] && row[9] != '') ? row[9].to_i : nil))
    end
  end

  def self.add_to_db(attrs)
    DB[:kettles].insert(attrs)
  end

  def self.update_in_db(id, attrs)
    DB[:kettles].where(id: id).update(attrs)
  end

  def self.delete_from_db(id)
    DB[:kettles].where(id: id).delete
  end
end
