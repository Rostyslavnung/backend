require 'sinatra'
require_relative '../models/kettle_type_list'

get '/types' do
  @types = KettleTypeList.new
  @types.read_from_db
  erb :'types'
end
