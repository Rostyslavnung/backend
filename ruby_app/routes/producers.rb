require 'sinatra'
require_relative '../models/producer_list'

get '/producers' do
  @producers = ProducerList.new
  @producers.read_from_db
  erb :'producers'
end
