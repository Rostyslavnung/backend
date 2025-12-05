require 'sinatra'
require 'sinatra/flash'
require 'sinatra/content_for'
require 'sequel'
require 'erb'
require 'bcrypt'
require_relative 'config/database'
require_relative 'models/base_entity'
require_relative 'models/base_list'
require_relative 'models/color'
require_relative 'models/color_list'

set :root, File.dirname(__FILE__)

class ClearInvalidSession
  def initialize(app)
    @app = app
  end

  def call(env)
    begin
      @app.call(env)
    rescue => e
      if e.message =~ /HMAC is invalid|Session cookie encryptor error/i
        env.delete('HTTP_COOKIE')
        return @app.call(env)
      end
      raise
    end
  end
end

use ClearInvalidSession

configure do
  enable :sessions

  set :bind, '0.0.0.0'
  set :port, ENV.fetch('PORT', 4567)

  if ENV.fetch('RACK_ENV', 'development') == 'production'
    set :protection, except: :frame_options
  else
    set :protection, except: [:frame_options, :host_authorization]
  end
end

helpers do
  def current_user
    return nil unless session[:user_id]
    if defined?(User)
      User.find(session[:user_id])
    else
      nil
    end
  end

  def authenticated?
    !!current_user
  end
end

helpers Sinatra::ContentFor

# load route files
Dir[File.join(settings.root, 'routes', '*.rb')].each { |f| require_relative f }

namespace = self
