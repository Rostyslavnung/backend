require 'sinatra'
require 'sinatra/flash'
require_relative '../models/user'

get '/auth/login' do
  erb :'login'
end

post '/auth/login' do
  username = params['username']
  password = params['password']

  user = User.find_by_username(username)
  if user && user.authenticate(password)
    session[:user_id] = user.id
    flash[:success] = 'Ви увійшли'
    redirect '/'
  else
    flash[:warning] = 'Неправильне ім’я користувача або пароль'
    redirect '/auth/login'
  end
end

get '/auth/logout' do
  session.clear
  flash[:success] = 'Ви вийшли'
  redirect '/'
end
