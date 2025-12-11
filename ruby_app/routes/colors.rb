require 'sinatra'
require 'sinatra/flash'
require_relative '../models/color_list'
require_relative '../models/color'

get '/colors' do
  @colors = ColorList.new
  @colors.read_from_db
  erb :'colors'
end
