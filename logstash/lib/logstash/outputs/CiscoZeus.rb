# encoding: utf-8
require "logstash/outputs/base"
require "logstash/namespace"
require "logstash/json"
require 'zeus/api_client'

# Outputs events to CiscoZeus 
class LogStash::Outputs::Ciscozeus < LogStash::Outputs::Base
  config_name "CiscoZeus"
  
  config :token, :validate => :string
  config :endpoint, :validate => :string, :default => "data04.ciscozeus.io"
  config :log_name, :validate => :string, :default => "logstash_data"
  
  concurrency :single

  public
  def register
    @zeus_client = Zeus::APIClient.new({
      :access_token => @token,
      :endpoint => @endpoint
    })
  end # def register

  public
  def multi_receive(events)
    result = @zeus_client.send_logs(@log_name, events)
    if not result.success? 
      STDERR.puts "Failed to send data to zeus: " + result.data.to_s
    end
  end # def receive
end # class LogStash::Outputs::Ciscozeus
