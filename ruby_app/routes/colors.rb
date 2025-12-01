require 'sinatra'
require 'sinatra/flash'
require_relative '../models/color_list'
require_relative '../models/color'

get '/colors' do
  @colors = ColorList.new
  data_file = File.expand_path('../../app/data/colors.csv', __dir__)
  unless File.exist?(data_file)
    data_file = File.expand_path('../data/colors.csv', __dir__)
  end
  @colors.read_from_csv(data_file) if File.exist?(data_file)
  erb :'colors'
end

post '/colors/save' do
  id = params['id'] && params['id'].to_i
  name = params['name']

  if id && id > 0
    ColorList.update_in_db(id, name) rescue nil
    flash[:success] = 'Колір оновлено'
  else
    ColorList.add_to_db(name) rescue nil
    flash[:success] = 'Колір додано'
  end

  redirect '/colors'
end

post '/colors/delete/:id' do
  id = params['id'].to_i
  ColorList.delete_from_db(id) rescue nil
  flash[:success] = 'Колір видалено'
  redirect '/colors'
end
