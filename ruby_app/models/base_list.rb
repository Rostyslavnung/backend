class BaseList
  include Enumerable

  def initialize
    @items = []
  end

  def all
    @items
  end

  def find_by_id(id)
    @items.find { |i| i.id == id }
  end
end
