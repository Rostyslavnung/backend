class BaseEntity
  attr_reader :id

  def initialize(id)
    @id = id
  end

  def display
    raise NotImplementedError, 'Subclasses must implement display'
  end

  def to_hash
    raise NotImplementedError, 'Subclasses must implement to_hash'
  end

  def to_xml
    raise NotImplementedError, 'Subclasses must implement to_xml'
  end
end
