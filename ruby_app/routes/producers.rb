require 'sinatra'
require_relative '../models/producer_list'

get '/producers' do
  @producers = ProducerList.new
  data_file = File.expand_path('../../app/data/producers.csv', __dir__)
  if File.exist?(data_file)
    @producers.read_from_csv(data_file)
  else
    @producers.read_from_db
  end
  erb :'producers'
end
