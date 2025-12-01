require 'cgi'
require_relative 'base_entity'

class Color < BaseEntity
  attr_accessor :name

  def initialize(id, name)
    super(id)
    @name = name
  end

  def to_s
    "Color ID: #{@id}, Name: #{@name}"
  end

  def update(name: nil)
    @name = name if name
  end

  def to_hash
    { id: id, name: name }
  end

  def to_xml
    "<color><id>#{id}</id><name>#{CGI.escapeHTML(name.to_s)}</name></color>"
  end
end
