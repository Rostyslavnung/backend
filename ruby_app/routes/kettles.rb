require 'sinatra'
require 'sinatra/flash'
require_relative '../models/kettle_list'
require_relative '../models/producer_list'
require_relative '../models/kettle_type_list'
require_relative '../models/color_list'
require_relative '../models/material_list'

get '/kettles' do
  q = params['q']
  producer = params['producer']
  sort = params['sort'] || 'name'

  @producers = ProducerList.new
  @producers.read_from_db

  @types = KettleTypeList.new
  @types.read_from_db

  @colors = ColorList.new
  @colors.read_from_db

  @materials = MaterialList.new
  @materials.read_from_db

  @kettles = KettleList.new
  @kettles.read_from_db(q: q, producer: producer, sort: sort)

  erb :'kettles'
end

post '/kettles/save' do
  id = params['id'] && !params['id'].empty? ? params['id'].to_i : nil
  attrs = {
    model_code: params['model'],
    name: params['name'],
    price: params['price'] && params['price'] != '' ? params['price'].to_f : nil,
    producer_id: params['producer'] && params['producer'] != '' ? params['producer'].to_i : nil,
    kettle_type_id: params['type'] && params['type'] != '' ? params['type'].to_i : nil,
    color_id: params['color'] && params['color'] != '' ? params['color'].to_i : nil,
    material_id: params['material'] && params['material'] != '' ? params['material'].to_i : nil,
    capacity: params['capacity'] && params['capacity'] != '' ? params['capacity'].to_f : nil,
    warranty_months: params['warranty_months'] && params['warranty_months'] != '' ? params['warranty_months'].to_i : nil
  }

  if id
    KettleList.update_in_db(id, attrs)
    flash[:success] = 'Чайник оновлено'
  else
    KettleList.add_to_db(attrs)
    flash[:success] = 'Чайник додано'
  end

  redirect '/kettles'
end

post '/kettles/delete/:id' do
  id = params['id'].to_i
  KettleList.delete_from_db(id)
  flash[:success] = 'Чайник видалено'
  redirect '/kettles'
end
