class BaseList
  include Enumerable

  def initialize
    @items = []
  end

  def each(&block)
    @items.each(&block)
  end

  def add(item)
    @items << item
  end

  def all
    @items
  end

  def find_by_id(id)
    @items.find { |i| i.id == id }
  end

  def to_xml
    raise NotImplementedError, 'Subclasses must implement to_xml'
  end
end
