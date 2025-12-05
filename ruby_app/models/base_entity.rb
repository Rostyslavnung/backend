class BaseEntity
  attr_reader :id

  def initialize(id)
    @id = id
  end

  def to_hash
    raise NotImplementedError, 'Subclasses must implement to_hash'
  end
end
