require 'sinatra'
require 'sinatra/flash'
require_relative '../models/kettle_list'
require_relative '../models/producer_list'
require_relative '../models/kettle_type_list'
require_relative '../models/color_list'
require_relative '../models/material_list'

get '/' do
  @producers = ProducerList.new
  @producers.read_from_db

  @types = KettleTypeList.new
  @types.read_from_db

  @colors = ColorList.new
  @colors.read_from_db

  @materials = MaterialList.new
  @materials.read_from_db

  @kettles = KettleList.new
  @kettles.read_from_db

  erb :'kettles'
end