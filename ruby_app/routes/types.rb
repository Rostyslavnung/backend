require 'sinatra'
require_relative '../models/kettle_type_list'

get '/types' do
  @types = KettleTypeList.new
  data_file = File.expand_path('../../app/data/kettleTypes.csv', __dir__)
  if File.exist?(data_file)
    @types.read_from_csv(data_file)
  else
    @types.read_from_db
  end
  erb :'types'
end
