require 'bcrypt'

class User
  include BCrypt

  attr_accessor :id, :username, :password_hash, :is_admin

  def initialize(id:, username:, password_hash:, is_admin: false)
    @id = id
    @username = username
    @password_hash = password_hash
    @is_admin = is_admin
  end

  def password
    @password ||= Password.new(password_hash)
  end

  def password=(new_password)
    @password = Password.create(new_password)
    @password_hash = @password.to_s
  end

  def self.find(id)
    row = DB[:users].where(id: id).first
    return nil unless row
    new(id: row[:id], username: row[:username], password_hash: row[:password_hash], is_admin: row[:is_admin])
  end

  def self.find_by_username(username)
    row = DB[:users].where(username: username).first
    return nil unless row
    new(id: row[:id], username: row[:username], password_hash: row[:password_hash], is_admin: row[:is_admin])
  end

  def authenticate(plain)
    password == plain
  end
end
