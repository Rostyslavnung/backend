require 'cgi'
require_relative 'base_entity'

class Color < BaseEntity
  attr_accessor :name

  def initialize(id, name)
    super(id)
    @name = name
  end

  def to_hash
    { id: id, name: name }
  end
end
