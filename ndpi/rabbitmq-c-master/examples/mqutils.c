/* vim:set ft=c ts=2 sw=2 sts=2 et cindent: */
/*
 * ***** BEGIN LICENSE BLOCK *****
 * Version: MIT
 *
 * Portions created by Alan Antonuk are Copyright (c) 2012-2013
 * Alan Antonuk. All Rights Reserved.
 *
 * Portions created by VMware are Copyright (c) 2007-2012 VMware, Inc.
 * All Rights Reserved.
 *
 * Portions created by Tony Garnock-Jones are Copyright (c) 2009-2010
 * VMware, Inc. and Tony Garnock-Jones. All Rights Reserved.
 *
 * Permission is hereby granted, free of charge, to any person
 * obtaining a copy of this software and associated documentation
 * files (the "Software"), to deal in the Software without
 * restriction, including without limitation the rights to use, copy,
 * modify, merge, publish, distribute, sublicense, and/or sell copies
 * of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
 * BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
 * ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 * ***** END LICENSE BLOCK *****
 */

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include <stdint.h>
#include <amqp_tcp_socket.h>
#include <amqp.h>
#include <amqp_framing.h>

#include "utils.h"
#include "mqutils.h"

int AmqpPublishKeyValuePairs(amqp_connection_state_t conn, char *exchange, char *routingkey, KeyValuePairType *table, int tableSize);
int InitAmqpConnection(amqp_connection_state_t *conn, char * hostname, unsigned short port, char *userName, char *passwd);

int InitAmqpConnection(amqp_connection_state_t *conn, char * hostname, unsigned short port, char *userName, char *passwd)
{
  int returnStatus = 1, status;
  amqp_socket_t *socket = NULL;
  *conn = amqp_new_connection();

  socket = amqp_tcp_socket_new(*conn);
  if (!socket) {
    returnStatus = 0;
    die("creating TCP socket");

  }

  status = amqp_socket_open(socket, hostname, port);
  if (status) {
    returnStatus = 0;
    die("Error in opening TCP socket");
	
  }

  die_on_amqp_error(amqp_login(*conn, "/", 0, 131072, 0, AMQP_SASL_METHOD_PLAIN, "testuser", "testuser"),
                    "Logging in");
  amqp_channel_open(*conn, 1);
  die_on_amqp_error(amqp_get_rpc_reply(*conn), "Opening channel");

  return (returnStatus);


}

int CloseAmqpConnection(amqp_connection_state_t conn)
{
  die_on_amqp_error(amqp_channel_close(conn, 1, AMQP_REPLY_SUCCESS), "Closing channel");
  die_on_amqp_error(amqp_connection_close(conn, AMQP_REPLY_SUCCESS), "Closing connection");
  die_on_error(amqp_destroy_connection(conn), "Ending connection");
 
}

int AmqpPublishMessage(amqp_connection_state_t conn, char *exchange, char *routingkey, unsigned char *message)
{
    amqp_basic_properties_t props;
    props._flags = AMQP_BASIC_CONTENT_TYPE_FLAG | AMQP_BASIC_DELIVERY_MODE_FLAG;
    props.content_type = amqp_cstring_bytes("text/plain");
    props.delivery_mode = 2; /* persistent delivery mode */
    die_on_error(amqp_basic_publish(conn,
                                    1,
                                    amqp_cstring_bytes(exchange),
                                    amqp_cstring_bytes(routingkey),
                                    0,
                                    0,
                                    &props,
                                    amqp_cstring_bytes(message)),
                 "Publishing");
 
}

int main(int argc, char const *const *argv)
{
  char *hostname;
  int port, status;
  char *exchange;
  char *routingkey;
  char *message;
  amqp_socket_t *socket = NULL;
  amqp_connection_state_t conn;
  KeyValuePairType entries[20], *entryPtr;


  if (argc < 5) {
    fprintf(stderr, "Usage: mqutils host port exchange routingkey \n");
    return 1;
  }

  hostname = (char *)argv[1];
  port = atoi(argv[2]);
  exchange = (char *)argv[3];
  routingkey = (char *)argv[4];
  
  /* test entries to check */
  strcpy(entries[0].key , "srcIp");
  entries[0].value = 0x0a060102;
  strcpy(entries[1].key , "destIp");
  entries[1].value = 0x0a060103;
  strcpy(entries[2].key , "srcPort");
  entries[2].value = 1024;
  strcpy(entries[3].key , "destPort");
  entries[3].value = 6000;
  strcpy(entries[4].key , "applicationPort");
  entries[4].value = 128;

  InitAmqpConnection(&conn, hostname,port, "testuser","testuser");
  AmqpPublishKeyValuePairs(conn,exchange,routingkey, entries, 5);
  //AmqpPublishMessage(conn,exchange,routingkey,"this is the third  message");
  CloseAmqpConnection(conn);


 return 0;
}


int AmqpPublishKeyValuePairs(amqp_connection_state_t conn, char *exchange, char *routingkey, KeyValuePairType *myTable, int tableSize)
{
	int i;
	amqp_basic_properties_t props;
    props._flags = AMQP_BASIC_CONTENT_TYPE_FLAG | AMQP_BASIC_DELIVERY_MODE_FLAG |  AMQP_BASIC_HEADERS_FLAG;
    props.content_type = amqp_cstring_bytes("text/plain");
    props.delivery_mode = 2; /* persistent delivery mode */
    amqp_table_t *table=&props.headers;
    props.headers.num_entries=tableSize;
    props.headers.entries=calloc(props.headers.num_entries, sizeof(amqp_table_entry_t));
    for (i=0;i<tableSize;i++)
    {
		(table->entries[i]).key = amqp_cstring_bytes(myTable[i].key);
    	((table->entries[i]).value).kind=AMQP_FIELD_KIND_I32;
    	((table->entries[i]).value).value.i32=myTable[i].value;
		
    }
    amqp_basic_publish(conn, 1,
                          amqp_cstring_bytes(exchange),
                          amqp_cstring_bytes(routingkey),
                          0,
                          0,
                          &props,
				 amqp_cstring_bytes((char *)table->entries));
	return 1; 
}
