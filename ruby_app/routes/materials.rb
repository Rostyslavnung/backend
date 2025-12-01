require 'sinatra'
require_relative '../models/material_list'

get '/materials' do
  @materials = MaterialList.new
  data_file = File.expand_path('../../app/data/materials.csv', __dir__)
  if File.exist?(data_file)
    @materials.read_from_csv(data_file)
  else
    @materials.read_from_db
  end
  erb :'materials'
end
