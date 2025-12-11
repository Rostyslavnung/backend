require 'sinatra'
require_relative '../models/material_list'

get '/materials' do
  @materials = MaterialList.new
  @materials.read_from_db
  erb :'materials'
end
